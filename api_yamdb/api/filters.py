import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact',
        distinct=True)
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )

    class Meta:
        model = Title
        fields = [
            'name',
            'year',
            'genre',
            'category'
        ]
