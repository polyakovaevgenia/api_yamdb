from django.core.exceptions import ValidationError
from django.utils import timezone


def validator_year(year):
    if year > timezone.now().year:
        raise ValidationError('Невозможно указать год в будущем.')
