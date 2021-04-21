from django.urls import path

from items.views import detail_item

urlpatterns = [
    path('item/<int:pk>/', detail_item, name='detail_item')
]