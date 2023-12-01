from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title
from users.permissions import (IsAdmin, IsAdminOrReadOnly,
                               IsAuthorStaffOrReadOnly,
                               IsAdminOrReadOnly,)

from .pagination import CustomPagination
from .serializers import CategorySerializer, GenreSerializer, TitleSerilizer


class GenreCategoryViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """Базовый ViewSet для модели Genre и Category."""
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'destroy':
            return (IsAdmin(),)
        return super().get_permissions()


class GenreViewSet(GenreCategoryViewSet):
    """ViewSet для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryViewSet):
    """ViewSet для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerilizer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )
