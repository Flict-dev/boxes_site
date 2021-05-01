from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
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


class CartItemViewSet(viewsets.GenericViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def recount_cart(self):
        cart = Cart.objects.get(user=self.request.user)
        recount_cart(cart)

    def get_obj(self, pk):
        try:
            obj = CartItem.objects.get(id=pk)
            return obj
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        queryset = CartItem.objects.filter(cart=cart)
        return queryset

    def retrieve(self, request, pk=None):
        try:
            obj = CartItem.objects.get(id=pk)
            serializer = CartItemSerializer(obj)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            queryset = CartItem.objects.filter(cart=cart)
            objects = self.paginate_queryset(queryset)
            serializer = CartItemSerializer(objects, many=True)
            return self.get_paginated_response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
                self.recount_cart()
                serializer = CartItemSerializer(new_cart_item)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(cart_item.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        obj = self.get_obj(pk)
        serializer = CartItemSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.recount_cart()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        obj = self.get_obj(pk)
        serializer = CartItemSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.recount_cart()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        obj = self.get_obj(pk)
        obj.delete()
        self.recount_cart()
        return Response(status=status.HTTP_204_NO_CONTENT)
