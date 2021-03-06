from rest_framework import serializers
from kitchen_display.models import Order, OrderToDishes, Dish, Color
import pytz


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize the order model so it can be sent via the api
        to the local application
        In order for the entire model to be sent, we also need to serialize
        the different models that are attached to it such as the dishes
    """
    shop_name = serializers.SerializerMethodField('get_shop_name')
    shop_slug = serializers.SerializerMethodField('get_shop_slug')
    fetched_hour = serializers.SerializerMethodField('get_fetched_hour')
    arrival_hour = serializers.SerializerMethodField('get_arrival_hour')
    dishes = serializers.SerializerMethodField('get_dishes')
    color = serializers.SerializerMethodField('get_color')

    def get_color(self, order):
        return ColorSerializer(
            order.color,
            context={"request": self.context["request"]},
            many=False
        ).data

    def get_dishes(self, order):
        return OrderToDishesSerializer(
            order.ordertodishes_set.all().order_by("dish__name"),
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
            "arrival_hour", "delayed", "dishes", "customer", "arrival_hour", "color",
            "preparing_hour"
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


class ColorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Color
        fields = (
            'id', 'name', 'hex_or_rgba', 'position'
        )
