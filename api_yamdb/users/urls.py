from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APISignUp, UserViewSet, APIToken

router = DefaultRouter()

router.register('users', UserViewSet, 'user')

urlpatterns = [
    path('auth/signup/', APISignUp.as_view()),
    path('auth/token/', APIToken.as_view()),
    path('', include(router.urls)),
]
