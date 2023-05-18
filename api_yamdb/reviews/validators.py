from django.core.exceptions import ValidationError
from django.utils import timezone


def validator_year(year):
    if year > timezone.now().year or year < 0:
        raise ValidationError('Некорректно введен год!')
