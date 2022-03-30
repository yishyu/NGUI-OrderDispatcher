from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from kitchen_display.models import Order

@login_required
def kitchen_display(request):
    preparing_orders = Order.objects.filter(order_state="b")
    print(preparing_orders)
    return render(request, "kitchen_display.html", locals())
