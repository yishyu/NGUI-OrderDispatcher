from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from kitchen_display.decorators import require_api_key
from kitchen_display.models import Order
import kitchen_display.serializers as kds_serializers


@require_key
@api_view(['GET'])
def GetQueuedOrders(request, shop=shop):
    orders_in_preparation = Order.objects.filter(shop=shop, state="b").order_by("fetched_time")
    orders = Order.objects.filter(shop=shop, state="a").order_by("fetched_time")
    serialized_orders = kds_serializers.OrderSerializer(orders, context={'request': request, many=True})
    return HttpResponse(serialized_orders.data)
