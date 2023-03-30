from csv import DictReader
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


User = get_user_model()

DATASET = {
    # User: 'users.csv',
    # Category: 'category.csv',
    # Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            for model, file in DATASET.items():
                with open(
                    f'{settings.BASE_DIR}/static/data/{file}',
                    mode='r',
                    encoding='utf-8',
                ) as f:
                    reader = DictReader(f)
                    model.objects.bulk_create(
                        model(**data) for data in reader
                    )
            self.stdout.write('Данные успешно загружены')
        except Exception as error:
            self.stdout.write(
                f'Возникла ошибка во время загрузки файла '
                f'{file}: {error}'
            )
