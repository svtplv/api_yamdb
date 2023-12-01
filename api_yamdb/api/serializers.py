from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Title


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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
