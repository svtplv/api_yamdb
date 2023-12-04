from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


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
        return rating_reviews.get('avg_rating')

    def to_representation(self, instance):
        representation = super(
            TitleSerilizer, self).to_representation(instance)
        representation['genre'] = GenreSerializer(
            instance.genre, many=True).data
        representation['category'] = CategorySerializer(instance.category).data
        return representation


class ReviewUpdateSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class ReviewSerializer(ReviewUpdateSerializer):
    def validate(self, data):
        request = self.context['request']
        author_id = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
            author=author_id, title=title_id
        ).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв к одному произведению'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
