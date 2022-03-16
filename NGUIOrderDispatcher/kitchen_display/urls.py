from django.urls import path
import kitchen_display.views as views

urlpatterns = [
    path('', views.kitchen_display, name="kitchen_display_view"),
]
