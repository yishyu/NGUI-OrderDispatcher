from django.contrib import admin
from kitchen_display.models import Shop, Order, Dish, Category, OrderToDishes
from django.contrib.auth.models import User


# Register your models here.
class UserInline(admin.TabularInline):
    model = User


class ShopAdmin(admin.ModelAdmin):
    list_display = (
        "id", "slug", "name",
    )
    list_filter = ("name", )
    inline = (UserInline, )


class OrderToDishesInline(admin.TabularInline):
    model = OrderToDishes


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "order_id", "fetched_time", "arrival_time", "shop", "price", "order_type", "address", "order_state"
    )
    list_filter = ("shop", )
    inlines = (OrderToDishesInline, )


class DishAdmin(admin.ModelAdmin):
    list_display = (
        "name", "identifier", "category",
    )
    list_filter = ("name", "category")


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name",
    )
    list_filter = ("name", )


admin.site.register(Shop, ShopAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Category, CategoryAdmin)
