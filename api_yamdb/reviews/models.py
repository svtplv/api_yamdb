from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from users.models import User


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
                               validators=[MaxValueValidator(
                                   timezone.now().year)],
                               help_text='Год не может быть больше текущего')
    description = models.TextField('Описание',
                                   blank=True)
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


class Review(models.Model):
    title = models.ForeignKey(Title,
                              verbose_name='Произведение',
                              related_name='reviews',
                              on_delete=models.CASCADE,
                              null=True)
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(User,
                               verbose_name='Автор отзыва',
                               related_name='reviews',
                               on_delete=models.CASCADE,
                               null=True)
    score = models.IntegerField(verbose_name='Оценка',
                                validators=(MinValueValidator(1),
                                            MaxValueValidator(10),))
    pub_date = models.DateTimeField(verbose_name='Дата отзыва',
                                    auto_now_add=True,)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (models.UniqueConstraint(
            fields=('author', 'title'),
            name='Каждый автор может написать только один отзыв'),)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='Автор комментария',
                               related_name='comments',
                               on_delete=models.CASCADE,
                               null=True)
    title = models.ForeignKey(Title,
                              verbose_name='Произведение',
                              related_name='comments',
                              on_delete=models.CASCADE,
                              null=True)
    review = models.ForeignKey(Review,
                               verbose_name='Отзыв',
                               related_name='comments',
                               on_delete=models.CASCADE,
                               null=True)
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(verbose_name='Дата отзыва',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
