from django.conf import settings
from django.db import models

from users.models import User
from .validators import validate_score, validate_year


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=settings.MAX_REVIEWS_NAME
    )
    slug = models.SlugField(
        'Slug категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=settings.MAX_REVIEWS_NAME
    )
    slug = models.SlugField(
        'Slug жанра',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=settings.MAX_REVIEWS_NAME
    )
    year = models.IntegerField(
        'Год',
        validators=(validate_year,)
    )
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['year', 'name']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    score = models.SmallIntegerField(
        'Оценка',
        validators=(validate_score,)
    )
    pub_date = models.DateTimeField('Дата отзыва', auto_now_add=True,)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='Каждый автор может написать только один отзыв'
            ),
        )
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField('Дата отзыва', auto_now_add=True,
                                    db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
