from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import TitleViewSet


router = DefaultRouter()
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
