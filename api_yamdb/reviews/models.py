from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User

MIN_SCORE = 1
MAX_SCORE = 10
DEFAULT_SCORE = 1


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Ссылка', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField('Ссылка', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год')
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle'
    )
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
        ordering = ['-id']
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE, verbose_name='жанры')

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
        ordering = ['-pub_date']


class Review(BaseReviewCommentModel):
    score = models.PositiveSmallIntegerField(
        'Оценка', default=DEFAULT_SCORE,
        validators=[
            MinValueValidator(MIN_SCORE, (f'Минимальная оценка {MIN_SCORE}')),
            MaxValueValidator(MAX_SCORE, (f'Максимальная оценка {MAX_SCORE}'))
        ]
    )

    class Meta(BaseReviewCommentModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
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
