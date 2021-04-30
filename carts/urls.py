from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CartViewSet, CartItemViewSet

carts_urlpatterns = [
    path('', CartViewSet.as_view({'get': 'retrieve'}), name='carts')
]

router = DefaultRouter()
router.register('items', CartItemViewSet, basename='cart-items')
carts_urlpatterns += router.urls

urlpatterns = [
    path('carts/', include(carts_urlpatterns))
]
