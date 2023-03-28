from django.contrib.auth import get_user_model
from django.db import models

from api_yamdb.api_yamdb.settings import TEXT_LENGTH


class Review(models.Model):
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
    score = models.IntegerField('Оценка')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Comments(models.Model):
    review_id = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    text = models.TextField('Комментарий')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Title(models.Model):
    ...
