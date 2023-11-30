from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CategoryViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
