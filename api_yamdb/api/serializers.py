from rest_framework import serializers
from reviews.models import Genre, Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)