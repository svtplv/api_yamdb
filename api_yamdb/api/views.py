from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from reviews.models import Category, Genre, Review, Title
from users.permissions import (IsAdmin, IsAdminOrReadOnly,
                               IsAuthorStaffOrReadOnly)

from .pagination import CustomPagination
from .serializers import (CategorySerializer, CommentSerializer,
                          ReviewSerializer, ReviewUpdateSerializer,
                          GenreSerializer, TitleSerilizer)


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
    permission_classes = (IsAuthorStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action not in ('list', 'retrieve',):
            return (IsAuthorStaffOrReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id', 'title__id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id', 'title__id')
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review."""
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy',):
            return (IsAuthorStaffOrReadOnly(),)
        if self.action == 'create':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
