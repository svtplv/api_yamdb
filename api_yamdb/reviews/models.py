from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator

current_year = datetime.now().year


class Category(models.Model):
    name = models.CharField('Название категории',
                            max_length=256)
    slug = models.SlugField('Slug категории',
                            unique=True,
                            max_length=50,)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра',
                            max_length=256)
    slug = models.SlugField('Slug жанра',
                            unique=True,
                            max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения',
                            max_length=256)
    year = models.IntegerField('Год',
                               validators=[MaxValueValidator(current_year)],
                               help_text='Год не может быть больше текущего')
    description = models.TextField('Описание',
                                   blank=False)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='titles')
    genre = models.ManyToManyField(Genre,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='titles')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
