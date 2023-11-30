import csv
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import Title, Genre, Category, Review, Comment

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт данных CSV файлов в базу данных'

    model_classes = {
        'category': Category,
        'comments': Comment,
        # 'genre_title': TitleGenre,
        'genre': Genre,
        'review': Review,
        'titles': Title,
        'users': User
    }

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV-файл для загрузки')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.import_data(csv_file)

    def import_data(self, csv_file):
        """Функция загрузки CSV-файла и сохрания в базу данных."""
        model_name = os.path.splitext(os.path.basename(csv_file))[0]
        model_class = self.model_classes[model_name]

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                instance = model_class()
                for field, value in row.items():
                    setattr(instance, field, value)
                instance.save()

            self.stdout.write(self.style.SUCCESS(f'Данные из {csv_file} успешно загружены'))
    
