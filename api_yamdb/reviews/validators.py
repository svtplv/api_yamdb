from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_score(value):
    if not 1 <= value <= 10:
        raise ValidationError('Оценка может быть только от 1 до 10')


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError('Год не может быть больше текущего')
