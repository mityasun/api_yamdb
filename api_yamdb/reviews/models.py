from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Ссылка', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField('Ссылка', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год')
    description = models.TextField('Описание')
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genre',
        verbose_name='жанр'
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
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    score = models.IntegerField(
        'Оценка', validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
