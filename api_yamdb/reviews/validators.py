import datetime as dt
from django.core.exceptions import ValidationError


class ValidateTitleYear:
    """Валидатор для года произведения."""

    def validate_year(self, year):
        now = dt.date.today().year
        if year > now:
            raise ValidationError('Такой год еще не наступил.')
        return year
