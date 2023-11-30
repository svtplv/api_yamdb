from rest_framework import (mixins,
                            viewsets,
                            filters)

from reviews.models import Category
from .serializers import CategorySerializer
from users.permissions import IsAdminOrReadOnly, IsAdmin
from .pagination import CustomPagination


class GenreCategoryViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """Базовый ViewSet для модели Genre и Category."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'destroy':
            return (IsAdmin(),)
        return super().get_permissions()


class CategoryViewSet(GenreCategoryViewSet):
    """ViewSet для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
