from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ObjectDoesNotExist
from carts.models import Cart, CartItem
from carts.serializers import CartSerializer, CartItemSerializer
from carts.utils import recount_cart

"""
P.S. Я мог бы просто унаследоваться от классов, но так скучно и не понятно. Я просто хочу занть как это работает под капотом,
поэтому и стал изобретать свой велоспиед. Мог бы посмотреть и показать, как правильно это делать? 
И ещё, я знаю про функцию get_object_or_404, но люблю try except
"""


class CartViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                serializer = CartSerializer(cart)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(user=request.user)
                serializer = CartSerializer(cart)
                return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # def create(self, request):


class CartItemViewSet(viewsets.GenericViewSet):
    serializer_class = CartItemSerializer
# Добавить permission_classes, разобраться с users.

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            try:
                cart_item = CartItem.objects.get(id=pk)
                serializer = CartSerializer(cart_item)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        queryset = CartItem.objects.filter(cart=cart)
        return queryset

    def list(self, request):
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                queryset = CartItem.objects.filter(cart=cart)
                objects = self.paginate_queryset(queryset)
                serializer = CartItemSerializer(objects, many=True)
                return self.get_paginated_response(serializer.data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        cart_item = CartItemSerializer(data=request.data)
        if cart_item.is_valid():
            try:
                cart = Cart.objects.get(user=request.user)
                new_cart_item = CartItem.objects.create(
                    quantity=cart_item.data['quantity'],
                    item_id=cart_item.data['item'],
                    cart=cart
                )
                cart.items.add(new_cart_item)
                recount_cart(cart)
                serializer = CartItemSerializer(new_cart_item)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(cart_item.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        if request.user.is_authenticated:
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.data)
                try:
                    cart = get_object_or_404(Cart, user=request.user)
                    cart_item = CartItem.objects.get(id=pk)
                    cart_item.delete()  # Здесь происходит момент замены - удаляем и создаем новый объект
                    cart_item = CartItem.objects.create(
                        item_id=serializer.data['item'],
                        quantity=serializer.data['quantity'],
                        cart=cart
                    )
                    response = CartItemSerializer(cart_item)
                    return Response(response.data, status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, pk):
        if request.user.is_authenticated:
            serializer = CartItemSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                cart_item = CartItem.objects.get(id=pk)
                cart_item.quantity = serializer.data['quantity']
                cart_item.save()
                response = CartItemSerializer(cart_item)
                return Response(response.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, pk)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
