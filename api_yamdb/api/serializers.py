from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class TitleSerilizer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        required=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        write_only=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        required=True,
        queryset=Category.objects.all(),
        write_only=True)
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
            raise serializers.ValidationError('Слишком длинное имя')
        return value

    def to_representation(self, instance):
        representation = super(
            TitleSerilizer, self).to_representation(instance)
        representation['genre'] = GenreSerializer(instance.genre, many=True).data
        representation['category'] = CategorySerializer(instance.category).data
        return representation

