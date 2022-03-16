from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def kitchen_display(request):
    return render(request, "kitchen_display.html", locals())