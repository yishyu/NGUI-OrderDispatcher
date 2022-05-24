from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from kitchen_display.models import Order, Shop, Color


@login_required  # redirects to the login page if the user is not logged
def kitchen_display(request):
    """
        renders the main page of this website
        gets the first shop associated to the user for now
    """
    shops = request.user.shop_set.all()
    shop = shops.first()
    preparing_orders = Order.objects.filter(shop=shop, order_state="b").order_by("-arrival_time")
    colors = Color.objects.all().order_by("position")
    return render(request, "kitchen_display.html", locals())
