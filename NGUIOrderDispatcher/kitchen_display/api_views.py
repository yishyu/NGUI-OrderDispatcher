from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from kitchen_display.decorators import require_app_key, require_shop_key, allowed_domain
from kitchen_display.models import Order, Dish, OrderToDishes
import kitchen_display.serializers as kds_serializers
import json


@api_view(['GET'])
@require_app_key
def getQueuedOrders(request, shop):
    """
        called by the local app to get new orders if it has less than 4 preparing orders
    """
    orders_in_preparation = Order.objects.filter(shop=shop, state="b").order_by("fetched_time")
    orders = Order.objects.filter(shop=shop, state="a").order_by("fetched_time")
    serialized_orders = kds_serializers.OrderSerializer(orders, context={'request': request}, many=True)
    return HttpResponse(serialized_orders.data)


@api_view(['POST'])
@require_app_key
def changeStateToPreparing(request, shop):
    """
        called by the local app to mark the accepted orders
        GetQueuedOrders sends 4 orders at a time but the app could reject some of them
    """
    return HttpResponse()


@api_view(['POST'])
@require_app_key
def incrementDoneQuantity(request, shop):
    """
        called by the local app everytime an item is scanned
    """
    return HttpResponse()


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
                order_id=order_json["order_hash"],
                arrival_time=order_json["expected_date"],
                shop=shop,
                price=order_json["final_price"],
                order_type=order_json["order_type"],
                address=order_json["delivery_address"],
                phone=order_json["phone"],
            )
            for dish_json in order_json['jsonized_dishes']:
                dish, _ = Dish.objects.get_or_create(name=dish_json["name"])
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
    return HttpResponse()


@api_view(['GET'])
@allowed_domain
@require_shop_key
def getCurrentPreparingOrders(request, shop):
    """
        Called by the js in the html view
    """
    return HttpResponse(serialized_orders.data)
