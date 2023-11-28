from django.shortcuts import render
from rest_framework import (filters,
                            viewsets,
                            permissions,
                            mixins)

from reviews.models import Title, Genre, Categories

class CategoriesGenresViewSet(mixins.ListModelMixin,  mixins.CreateModelMixin,
                              mixins.DestroyModelMixin, viewsets.GenericViewSet):
        
        pass


class TitleViewset(viewsets.ModelViewSet):
        queryset = Title.objects.all()
        serializer = 