from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from items.models import Item
from items.serializers import ItemSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ItemPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page-size'
    max_page_size = 4


class ItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemPageNumberPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering = ['weight', 'price']
    filterset_fields = ['weight', 'price']
