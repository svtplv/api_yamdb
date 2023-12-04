from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import APISignUp, APIToken, UserViewSet

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, 'user')

urlpatterns = [
    path('auth/signup/', APISignUp.as_view(), name='signup'),
    path('auth/token/', APIToken.as_view(), name='token'),
    path('', include(router_v1.urls)),
]
