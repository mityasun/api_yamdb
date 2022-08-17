import re

from django.core.exceptions import ValidationError


class ValidateUsername:
    """Валидаторы для username."""

    def validate_username(self, username):
        pattern = re.compile(r'^[\w.@+-]+')

        if pattern.fullmatch(username) is None:
            raise ValidationError('Некорректные символы в username!')
        elif username == 'me':
            raise ValidationError('Ник "me" нельзя регистрировать!')
        return username

