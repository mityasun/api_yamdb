from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genre')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Произведения"


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE)


class Review(models.Model):
    pass