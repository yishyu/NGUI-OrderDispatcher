from rest_framework import serializers
from kitchen_display.models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = (
            "id"
        )
