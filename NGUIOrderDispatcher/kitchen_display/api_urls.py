from django.conf.urls import include
from django.urls import path

import kitchen_display.api_views as views
app_name = 'kitchen_display'
urlpatterns = [
    path('GetQueuedOrders/', views.getOrders, name="getOrders"),
]