from django.contrib import admin

from shop.models import Product, Order, ShoppingCart


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'count']
    list_filter = ['category']
    search_fields = ['title']
    fields = ['title', 'description', 'category', 'image', 'price', 'count']

class ShoppingCartInLine(admin.TabularInline):
    model = ShoppingCart.orders.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [
        ShoppingCartInLine,
    ]


