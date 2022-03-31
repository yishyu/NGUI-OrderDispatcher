from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from kitchen_display.models import Order, Shop

@login_required
def kitchen_display(request):
    shops = request.user.shop_set.all()
    shop = shops.first()
    preparing_orders = Order.objects.filter(shop=shop, order_state="b").order_by("-arrival_time")
    print(preparing_orders)
    return render(request, "kitchen_display.html", locals())
