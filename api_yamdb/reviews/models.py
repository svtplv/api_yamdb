from django.db import models


class Category(models.Model):
    """Модель Category."""
    name = models.CharField(max_length=128, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

        def __str__(self):
            return self.name


class Genre(models.Model):
    """Модель Genre."""
    name = models.CharField(max_length=128, verbose_name='Название жанра')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

        def __str__(self):
            return self.name


class Title(models.Model):
    """Модель Title."""
    name = models.CharField(max_length=128,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='categoryes')
    genre = models.ManyToManyField(Genre, on_delete=models.SET_NULL,
                                   null=True,)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

        def __str__(self):
            return self.name
