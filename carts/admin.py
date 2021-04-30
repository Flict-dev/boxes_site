from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'price', 'quantity', 'in_order')
    list_filter = ('user', 'in_order')
    raw_id_fields = ('items',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'cart', 'price', 'quantity')
    list_filter = ('item', 'cart')
