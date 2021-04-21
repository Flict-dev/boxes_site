from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from items.models import Item


@api_view(http_method_names=['GET'])
def detail_item(request, pk):
    try:
        response = Item.objects.get(id=pk)
        return Response({
            "id": response.id,
            "title": response.title,
            "description": response.description,
            "image": str(response.image),
            "weight": response.weight,
            "price": response.price,
            "size": response.size,
        })
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
