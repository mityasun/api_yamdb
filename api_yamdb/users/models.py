from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    email = models.EmailField('Почта', max_length=254, unique=True)
    username = models.CharField('Никнэйм', max_length=30, unique=True)
    password = models.CharField('Пароль', max_length=15, null=True, blank=True)
    role = models.CharField('Роль', max_length=30, choices=ROLES, default=USER)
    bio = models.TextField('Об авторе', max_length=500, null=True, blank=True)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
