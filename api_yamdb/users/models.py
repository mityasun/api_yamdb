from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('Почта', max_length=254, unique=True)
    bio = models.TextField('Биография', max_length=500, null=True, blank=True)
    role = models.CharField('Роль', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
