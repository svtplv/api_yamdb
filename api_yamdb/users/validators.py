import re

from django.core.exceptions import ValidationError
from django.conf import settings


def validate_username(value):
    if value in settings.FORBIDDEN_WORDS:
        raise ValidationError(f'Имя пользователя не может быть {value}')

    if not re.fullmatch(r'[\w.@+-]+', value):
        raise ValidationError(
            'Имя пользователя должно состоять из букв/цифр/'
            'символов @.+-_'
        )
