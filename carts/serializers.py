from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from carts.models import Cart, CartItem


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
