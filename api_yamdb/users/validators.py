import re

from django.core.exceptions import ValidationError


class ValidateUsername:
    """Валидаторы для username."""

    def validate_username(self, username):
        """Валидация, что нельзя регистрировать username me."""

        if username == 'me':
            raise ValidationError('Ник "me" нельзя регистрировать!')
        return username


    def validate_symbols(self, username):
        """Валидация допустимых символов в username."""

        if re.match(r"^[\w.@+-]+\z", username) is None:
            raise ValidationError('Некорректные символы в username!')
        return username
