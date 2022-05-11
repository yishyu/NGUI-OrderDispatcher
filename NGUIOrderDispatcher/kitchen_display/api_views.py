from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from kitchen_display.decorators import require_app_key, require_shop_key
from kitchen_display.models import Order, Dish, OrderToDishes, Shop, Color
import kitchen_display.serializers as kds_serializers
import json
import datetime
import pytz


@api_view(['GET'])
@require_app_key
def getQueuedOrders(request, shop):
    """
        called by the local app to get new orders if it has less than 4 preparing orders
        the logic is implemented in the local app
    """
    local_tz = pytz.timezone('Europe/Brussels')
    data = json.loads(request.data)
    amount = int(data.get('amount', 0))  # limit the amount of result in the qs
    orders = Order.objects.filter(shop=shop, order_state="a").order_by("arrival_time")[:amount]
    colors = list(Color.objects.all().exclude(order__order_state="b"))
    for order in orders:
        order.order_state = "b"
        order.switched_to_preparing_time = datetime.datetime.now().astimezone(local_tz)
        order.color = colors.pop()
        order.save()
    serialized_orders = kds_serializers.OrderSerializer(orders, context={'request': request}, many=True)
    return Response(serialized_orders.data)


@api_view(['GET'])
@require_app_key
def getCurrentPreparingOrders(request, shop):
    """
        Called by the js in the html view
    """
    preparing_orders = Order.objects.filter(shop=shop, order_state="b").order_by("color__position")  # displayed from left to right. The left one must be the latest one
    serialized_orders = kds_serializers.OrderSerializer(preparing_orders, context={'request': request}, many=True)
    return Response(serialized_orders.data)


@api_view(['GET'])
def siteGetCurrentPreparingOrders(request, shop_pk):
    shop = Shop.objects.get(pk=shop_pk)
    preparing_orders = Order.objects.filter(shop=shop, order_state="b").order_by("color__position")  # displayed from left to right. The left one must be the latest one
    serialized_orders = kds_serializers.OrderSerializer(preparing_orders, context={'request': request}, many=True)
    return Response(serialized_orders.data)


@api_view(['POST'])
@csrf_exempt
@require_app_key
def changeStateToDone(request, shop):
    """
        called by the local app to mark the accepted orders
    """
    data = json.loads(request.data)
    order_id = data.get("order", None)
    if not order_id:
        response = Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        Order.objects.filter(id=order_id).update(order_state="c")
        response = Response(status=status.HTTP_200_OK)
    return response


@api_view(['POST'])
@require_app_key
def incrementDoneQuantity(request, shop):
    """
        called by the local app everytime an item is scanned
    """
    data = json.loads(request.data)
    [order_id, dish_identifier] = data.get("order", [None, None])  # "order": [order_id, dish_identifier]
    if not (order_id and dish_identifier):
        response = Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        o2d = Order.objects.get(id=order_id).ordertodishes_set.get(dish__identifier=dish_identifier)
        o2d.quantity_done += 1
        o2d.save()
        response = Response(status=status.HTTP_202_ACCEPTED)
    return response


@api_view(['POST'])
@csrf_exempt
@require_shop_key
def addNewOrders(request, shop):
    """
        Called by an external cron script running on the server
    """
    data = json.loads(request.data)
    for order_json in data['online']:
        order_qs = Order.objects.filter(order_id=order_json['order_hash'])
        if order_qs.count() == 0:
            order = Order.objects.create(
                customer=order_json["user_username"],
                order_id=order_json["order_hash"],
                arrival_time=order_json["expected_date"],
                shop=shop,
                price=order_json["final_price"],
                order_type=order_json["order_type"],
                address=order_json["delivery_address"],
                phone=order_json["phone"],
            )
            for dish_json in order_json['jsonized_dishes']:
                dish, _ = Dish.objects.get_or_create(name=dish_json["name"], identifier=dish_json["identifier"])
                o2d, created = OrderToDishes.objects.get_or_create(
                    order=order,
                    dish=dish
                )
                if created:
                    o2d.quantity = dish_json["quantity"]
                else:
                    o2d.quantity += dish_json["quantity"]
                o2d.save()

                # sauces & accompaniment considered as dishes
                if dish_json["accompaniment"] != 'None':
                    dish, _ = Dish.objects.get_or_create(name=dish_json["accompaniment"])
                    o2d, created = OrderToDishes.objects.get_or_create(
                        order=order,
                        dish=dish
                    )
                    if created:
                        o2d.quantity = dish_json["quantity"]
                    else:
                        o2d.quantity += dish_json["quantity"]
                    o2d.save()
                if dish_json["sauce"] != "None":
                    dish, _ = Dish.objects.get_or_create(name=dish_json["sauce"])
                    o2d, created = OrderToDishes.objects.get_or_create(
                        order=order,
                        dish=dish
                    )
                    if created:
                        o2d.quantity = dish_json["quantity"]
                    else:
                        o2d.quantity += dish_json["quantity"]
                    o2d.save()
    return Response(status=status.HTTP_201_CREATED)
