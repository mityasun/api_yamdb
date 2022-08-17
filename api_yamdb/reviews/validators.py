import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """Валидатор для года произведения."""
    current_year = dt.date.today().year
    if value > current_year:
        raise ValidationError('Такой год еще не наступил.')
    return value
