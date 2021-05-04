from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ObjectDoesNotExist
from carts.models import Cart, CartItem
from carts.serializers import CartSerializer, CartItemSerializer


class CartViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        cart, param = Cart.objects.get_or_create(user=request.user, defaults={"user": request.user})
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.GenericViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

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
                cart_item.save()
                cart.items.add(cart_item.data['id'])
                return Response(cart_item.data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(cart_item.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        obj = self.get_obj(pk)
        serializer = CartItemSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        obj = self.get_obj(pk)
        serializer = CartItemSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        obj = self.get_obj(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
