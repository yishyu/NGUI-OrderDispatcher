from rest_framework import serializers
from kitchen_display.models import Order, OrderToDishes, Dish
import pytz


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    shop_name = serializers.SerializerMethodField('get_shop_name')
    shop_slug = serializers.SerializerMethodField('get_shop_slug')
    fetched_hour = serializers.SerializerMethodField('get_fetched_hour')
    arrival_hour = serializers.SerializerMethodField('get_arrival_hour')
    dishes = serializers.SerializerMethodField('get_dishes')

    def get_dishes(self, order):
        return OrderToDishesSerializer(
            order.ordertodishes_set.all(),
            context={"request": self.context["request"]},
            many=True
        ).data

    @staticmethod
    def get_shop_slug(order):
        return order.shop.slug

    @staticmethod
    def get_shop_name(order):
        return order.shop.name

    @staticmethod
    def get_fetched_hour(order):
        """Returns the order's creation hour"""
        date = order.fetched_time
        local_tz = pytz.timezone('Europe/Brussels')
        date = date.astimezone(local_tz)
        return f"{str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}"

    @staticmethod
    def get_arrival_hour(order):
        """Returns the expected hour for the order to complete"""
        date = order.arrival_time
        local_tz = pytz.timezone('Europe/Brussels')
        date = date.astimezone(local_tz)
        return f"{str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}"

    class Meta:
        model = Order
        fields = (
            "pk", "order_id", "fetched_time", "arrival_time", "shop_name", 'shop_slug',
            "price", "order_type", "order_state", "time_since_arrival", "fetched_hour",
            "arrival_hour", "delayed", "dishes", "customer", "arrival_hour"
        )


class OrderToDishesSerializer(serializers.HyperlinkedModelSerializer):

    dish = serializers.SerializerMethodField('get_dish')

    def get_dish(self, o2d):
        return DishSerializer(
            o2d.dish,
            context={"request": self.context["request"]},
            many=False
        ).data

    class Meta:
        model = OrderToDishes
        fields = (
            'dish', 'quantity', 'quantity_done', 'quantity_left', 'done'
        )


class DishSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Dish
        fields = (
            'pk', 'name', 'category', 'identifier'
        )
