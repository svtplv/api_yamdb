import csv
import re

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Title, Genre, Category, Review, Comment


User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов в базу данных'

    def import_data(self, model, file_path):
        """Функция загрузки CSV-файла и сохрания в базу данных."""
        with open(f'static/data/{file_path}', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            reader.fieldnames = [
                re.sub(
                    r'(?P<field>category|author)',
                    r'\g<field>_id',
                    fieldname
                ) for fieldname in reader.fieldnames
            ]
            objects = [model(**object_data) for object_data in reader]
            model.objects.bulk_create(objects)

    def handle(self, *args, **options):
        MODEL_PATH = {
            User: 'users.csv',
            Category: 'category.csv',
            Genre: 'genre.csv',
            Title: 'titles.csv',
            Title.genre.through: 'genre_title.csv',
            Review: 'review.csv',
            Comment: 'comments.csv',
        }

        for model, file_path in MODEL_PATH.items():
            self.import_data(model, file_path)
            self.stdout.write(self.style.SUCCESS(
                f'Данные из {file_path} успешно загружены'))
