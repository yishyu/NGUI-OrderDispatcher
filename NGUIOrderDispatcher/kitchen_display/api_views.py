from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from kitchen_display.decorators import require_app_key, require_shop_key, allowed_domain
from kitchen_display.models import Order
import kitchen_display.serializers as kds_serializers


@require_app_key
@api_view(['GET'])
def getQueuedOrders(request, shop):
    """
        called by the local app to get new orders if it has less than 4 preparing orders
    """
    orders_in_preparation = Order.objects.filter(shop=shop, state="b").order_by("fetched_time")
    orders = Order.objects.filter(shop=shop, state="a").order_by("fetched_time")
    serialized_orders = kds_serializers.OrderSerializer(orders, context={'request': request}, many=True)
    return HttpResponse(serialized_orders.data)


@require_app_key
@api_view(['POST'])
def changeStateToPreparing(request, shop):
    """
        called by the local app to mark the accepted orders
        GetQueuedOrders sends 4 orders at a time but the app could reject some of them
    """
    return HttpResponse()


@require_app_key
@api_view(['POST'])
def incrementDoneQuantity(request, shop):
    """
        called by the local app everytime an item is scanned
    """
    return HttpResponse()

@require_shop_key
@api_view(['POST'])
def addNewOrders(request, shop):
    """
        Called by an external cron script running on the server
    """
    return HttpResponse(serialized_orders.data)


@allowed_domain
@require_shop_key
@api_view(['GET'])
def getCurrentPreparingOrders(request, shop):
    """
        Called by the js in the html view
    """
    return HttpResponse(serialized_orders.data)
