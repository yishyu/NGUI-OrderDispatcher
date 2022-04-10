from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.
class Shop(models.Model):
    slug = models.SlugField(max_length=126, null=False, unique=True, default='')
    local_application_api_key = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, blank=False)
    employees = models.ManyToManyField(User, verbose_name="user")

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.CharField("customer", max_length=50, default="")
    order_id = models.CharField("order id", max_length=50)
    dishes = models.ManyToManyField("Dish", verbose_name="dish", through="OrderToDishes")
    fetched_time = models.DateTimeField("fetched_time", auto_now=True, auto_now_add=False)
    arrival_time = models.DateTimeField("arrival_time", auto_now=False, auto_now_add=False, null=True)
    shop = models.ForeignKey("Shop", verbose_name="shop", on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    order_types = [
        ('a', 'Pick up'),
        ('b', 'Delivery')
    ]
    order_type = models.CharField("type", choices=order_types, max_length=50, null=True)
    address = models.CharField("address", max_length=200, null=True)
    phone = models.CharField(max_length=20, null=False, blank=False, default="0")
    order_states = [
        ("a", "In Queue"),
        ("b", "Preparing"),
        ("c", "Done"),
    ]
    order_state = models.CharField("state", choices=order_states, max_length=50, default="a")

    @property
    def time_since_arrival(self):
        time = datetime.datetime.now() - self.fetched_time.replace(tzinfo=None)
        return f"{str(time.seconds//3600).zfill(2)}:{str((time.seconds//60)%60).zfill(2)}:{str(time.seconds%60).zfill(2)}"

    @property
    def delayed(self):
        return datetime.datetime.now() > self.arrival_time.replace(tzinfo=None)

    def __str__(self):
        return self.order_id


class Dish(models.Model):
    name = models.CharField("name", max_length=50)
    category = models.ForeignKey("Category", verbose_name="category", on_delete=models.CASCADE, null=True)
    identifier = models.CharField("remote identifier", max_length=10, default="")

    def __str__(self):
        return self.name


class OrderToDishes(models.Model):
    order = models.ForeignKey("Order", verbose_name="order", on_delete=models.CASCADE)
    dish = models.ForeignKey("Dish", verbose_name="dish", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    quantity_done = models.IntegerField("quantity_done", default=0)

    @property
    def done(self):
        return self.quantity == self.quantity_done

    @property
    def quantity_left(self):
        return self.quantity - self.quantity_done


class Category(models.Model):
    name = models.CharField("category", max_length=150)

    def __str__(self):
        return self.name
