import json

from django.http import HttpResponseForbidden
from kitchen_display.models import Shop
from kitchen_display.utils import get_client_ip
from django.conf import settings


def require_app_key(func):
    def wrapper(request, *args, **kwargs):
        data = json.loads(request.data)
        key = data['key']
        key_obj = Shop.objects.filter(local_application_api_key=key)
        if key_obj.count() < 1:
            return HttpResponseForbidden()
        key_obj = key_obj.first()
        return func(request, shop=key_obj)
    return wrapper


def require_shop_key(func):
    def wrapper(request):
        data = json.loads(request.data)
        key = data['key']
        key_obj = Shop.objects.filter(slug=key)
        if key_obj.count() < 1:
            return HttpResponseForbidden()
        key_obj = key_obj.first()
        return func(request, shop=key_obj)
    return wrapper
