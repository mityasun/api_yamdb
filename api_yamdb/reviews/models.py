from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api_yamdb.settings import LEN_FOR_NAME
from users.models import User
from .base_models import BaseModelGenreCategory


class Category(BaseModelGenreCategory):
    name = models.CharField('Категория', max_length=LEN_FOR_NAME)

    class Meta(BaseModelGenreCategory.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(BaseModelGenreCategory):
    name = models.CharField('Жанр', max_length=LEN_FOR_NAME)

    class Meta(BaseModelGenreCategory.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=LEN_FOR_NAME)
    year = models.PositiveSmallIntegerField('Год')
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='жанры')

    def __str__(self):
        return f'{self.title} {self.genre}'

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class BaseReviewCommentModel(models.Model):
    """Базовый абстрактный класс для Review и Comment."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self) -> str:
        return self.text[:settings.CUT_TEXT]

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(BaseReviewCommentModel):
    score = models.PositiveSmallIntegerField(
        'Оценка', default=settings.DEFAULT_SCORE,
        validators=[
            MinValueValidator(
                settings.MIN_SCORE, f'Минимальная оценка {settings.MIN_SCORE}'
            ),
            MaxValueValidator(
                settings.MAX_SCORE, f'Максимальная оценка {settings.MAX_SCORE}'
            )
        ]
    )

    class Meta(BaseReviewCommentModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            )
        ]


class Comment(BaseReviewCommentModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )

    class Meta(BaseReviewCommentModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
