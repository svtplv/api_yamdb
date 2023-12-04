from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_score(value):
    if not settings.MIN_SCORE <= value <= settings.MAX_SCORE:
        raise ValidationError(
            f'Оценка может быть только от {settings.MIN_SCORE}'
            f'  до {settings.MAX_SCORE}'
        )


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError('Год не может быть больше текущего')
