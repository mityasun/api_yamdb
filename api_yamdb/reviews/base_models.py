from django.db import models
from api_yamdb.settings import LEN_FOR_SLUG, LEN_FOR_NAME


class BaseModelGenreCategory(models.Model):
    """Абстрактная модель для жанров и категорий."""

    name = models.CharField('Название', max_length=LEN_FOR_NAME)
    slug = models.SlugField('Ссылка', max_length=LEN_FOR_SLUG, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name
