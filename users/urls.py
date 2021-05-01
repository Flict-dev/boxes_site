from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from users.views import (
    RegisterAPIView,
    CurrentUserViewSet,
)

users_patterns = [
    path('auth/login/', views.obtain_auth_token),
    path('auth/register/', RegisterAPIView.as_view()),
    path('current/', CurrentUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}))
]

urlpatterns = [
    path('users/', include(users_patterns))
]
