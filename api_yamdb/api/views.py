from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .mixins import GenreCategoryMixin
from .permissions import IsAdminOrReadOnly, IsAuthorStaffOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          ReviewUpdateSerializer, TitleSerilizer)


class GenreViewSet(GenreCategoryMixin):
    """ViewSet для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryMixin):
    """ViewSet для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerilizer
    http_method_names = settings.ALLOWED_METHODS
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorStaffOrReadOnly, )
    http_method_names = settings.ALLOWED_METHODS

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(
            author=self.request.user, review=review
        )


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorStaffOrReadOnly,)
    http_method_names = settings.ALLOWED_METHODS
    """ViewSet для модели Review."""
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_title()
        )
