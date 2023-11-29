from rest_framework import serializers
from reviews.models import Title, Category, Genre
from django.db.models import Avg


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
            'category',)
        
    def get_rating(self, obj):
        rating_reviews = obj.reviews.aggregate(avg_rating=Avg('score'))
        if rating_reviews.get('avg_rating') is not None:
            return 0
        return rating_reviews.get('avg_rating')
