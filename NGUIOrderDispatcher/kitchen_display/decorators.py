import json

from django.http import HttpResponseForbidden
from kitchen_display.models import Shop


def require_api_key(func):
    def wrapper(request):
        data = json.loads(request.data)
        key = data['key']
        appKey = data['appKey']
        key_obj = Shop.objects.filter(slug=key, local_application_api_key=appKey)
        if key_obj.count() < 1:
            return HttpResponseForbidden()
        key_obj = key_obj.first()
        return func(request, shop=key_obj)
    return wrapper