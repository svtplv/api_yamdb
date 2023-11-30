from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CategoryViewSet, GenreViewSet, TitleViewSet


router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
