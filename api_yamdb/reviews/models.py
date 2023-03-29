from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

from .validators import validate_actuality_year

TEXT_LENGTH = 15


class Review(models.Model):
    class Score(models.TextChoices):
        ONE = 1, _('ONE')
        TWO = 2, _('TWO')
        THREE = 3, _('THREE')
        FOUR = 4, _('FOUR')
        FIVE = 5, _('FIVE')
        SIX = 6, _('SIX')
        SEVEN = 7, _('SEVEN')
        EIGHT = 8, _('EIGHT')
        NINE = 9, _('NINE')
        TEN = 10, _('TEN')

    title_id = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    text = models.TextField('Отзыв')
    score = models.IntegerField('Оценка', max_length=2, choices=Score.choices)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        validators=[validate_actuality_year],
        verbose_name='Год создания',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(app_label)s_%(class)s',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'
