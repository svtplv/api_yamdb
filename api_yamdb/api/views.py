from rest_framework import (viewsets,
                            filters)
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title
from .serializers import TitleSerilizer
from users.permissions import IsAuthorStaffOrReadOnly


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
        'year',)
