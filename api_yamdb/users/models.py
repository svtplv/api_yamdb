from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    MOD = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MOD, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.MAX_USERS_NAME,
        unique=True,
        validators=(validate_username,)
    )
    email = models.EmailField(
        'Почта',
        max_length=settings.MAX_EMAIL,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_USERS_NAME,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_USERS_NAME,
        blank=True,
    )
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField(
        'Роль',
        max_length=settings.MAX_ROLE,
        choices=ROLE_CHOICES,
        default=USER
    )

    @property
    def is_mod(self):
        return self.role == self.MOD

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
