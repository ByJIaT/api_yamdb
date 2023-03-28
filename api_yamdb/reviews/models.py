from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

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


class Title(models.Model):
    ...
