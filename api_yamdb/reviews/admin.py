from django.contrib import admin

from .models import Category, Title, Genre


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'year',
                    'category',
                    'genre', )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'slug', )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'slug', )
