from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


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
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[\w.@+-]+\Z',
                message=(
                    'Имя пользователя должно состоять из букв/цифр/'
                    'символов @.+-_'
                ),
                code='Некорректное имя'
            ),
        ],
    )
    email = models.EmailField('Почта', unique=True,)
    first_name = models.CharField('Имя', max_length=150, blank=True,)
    last_name = models.CharField('Фамилия', max_length=150, blank=True,)
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER)

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
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='username_not_me',
                violation_error_message='Введите имя отличное от "me"'
            )
        ]

    def __str__(self):
        return self.username
