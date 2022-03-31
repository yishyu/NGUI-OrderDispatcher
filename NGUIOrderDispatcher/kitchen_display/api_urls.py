from django.conf.urls import include
from django.urls import path

import kitchen_display.api_views as views
app_name = 'kitchen_display'
urlpatterns = [
    path('getqueuedorders', views.getQueuedOrders, name="getQueuedOrders"),
    path("'changestatetopreparing", views.changeStateToPreparing, name="changeStateToPreparing"),
    path('incrementdonequantity', views.incrementDoneQuantity, name="incrementDoneQuantity"),
    path('addneworders', views.addNewOrders, name="addNewOrders"),
    path('getcurrentpreparingorders/<int:shop_pk>', views.getCurrentPreparingOrders, name="getCurrentPreparingOrders"),
]
