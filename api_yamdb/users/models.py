from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import ValidateUsername


class User(AbstractUser, ValidateUsername):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    email = models.EmailField('Почта', max_length=settings.EMAIL, unique=True)
    username = models.CharField(
        'Никнэйм', max_length=settings.USERNAME_NAME, unique=True
    )
    role = models.CharField('Роль', max_length=30, choices=ROLES, default=USER)
    # не понимаю я как тут циклом в 1 строке пройтись, дай намек пожирней плиз:)
    bio = models.TextField('Об авторе', null=True, blank=True)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
