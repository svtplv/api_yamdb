from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Genre, Title


class TitleSerilizer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        required=True,
        slug_field='name',
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='name',
        required=True,
        queryset=Category.objects.all())
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        rating_reviews = obj.reviews.aggregate(avg_rating=Avg('score'))
        if rating_reviews.get('avg_rating') is not None:
            return 0
        return rating_reviews.get('avg_rating')
 
    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError('Длина названия произведения не может превышать 256 символов')
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
