from rest_framework import serializers
from kitchen_display.models import Order


class OrderSerializer(serializers.HyperLinkedModelSerializer):

    class Meta:
        model = Order
        fields = (
            "id"
        )