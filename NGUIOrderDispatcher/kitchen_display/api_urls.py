from django.conf.urls import include
from django.urls import path

import kitchen_display.api_views as views
app_name = 'kitchen_display'
urlpatterns = [
    path('getqueuedorders', views.getQueuedOrders, name="getQueuedOrders"),
    path("changeStateToDone", views.changeStateToDone, name="changeStateToDone"),
    path('incrementdonequantity', views.incrementDoneQuantity, name="incrementDoneQuantity"),
    path('addneworders', views.addNewOrders, name="addNewOrders"),
    path('getcurrentpreparingorders', views.getCurrentPreparingOrders, name="getCurrentPreparingOrders"),
    path('getcurrentpreparingorders/<int:shop_pk>', views.siteGetCurrentPreparingOrders, name="siteGetCurrentPreparingOrders"),

]
