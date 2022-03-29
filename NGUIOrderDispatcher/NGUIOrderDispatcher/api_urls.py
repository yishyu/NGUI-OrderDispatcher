from django.conf.urls import include
from django.urls import path

import NGUIOrderDispatcher.api_views as views
app_name = 'api'
urlpatterns = [
    path('kitchen_display/', include("kitchen_display.api_urls", namespace="kitchen_display")),
]