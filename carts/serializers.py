from django.db.models import Sum
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from carts.models import Cart, CartItem
from items.serializers import ItemSerializer


class CartItemSerializer(ModelSerializer):
    total_price = serializers.SerializerMethodField('_get_total_price')
    item = ItemSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'item_id', 'price', 'quantity', 'total_price')

    def _get_total_price(self, cart_item):
        return cart_item.price * cart_item.quantity

    def create(self, validated_data):
        cart_item = CartItem(
            item=validated_data['item'],
            price=validated_data['item'].price,
            quantity=validated_data['quantity'],
        )
        cart_item.save()
        return cart_item


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField('_get_total_cost')

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_cost')

    def _get_total_cost(self, cart):
        cart_items = CartItemSerializer(cart.items, many=True)
        total_cost = 0
        for item in range(cart.items.count()):
            total_cost += cart_items.data[item]['total_price']
        return total_cost
