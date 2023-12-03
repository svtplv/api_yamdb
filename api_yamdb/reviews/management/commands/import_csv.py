import csv
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import Title, Genre, Category, Review, Comment

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт данных CSV файлов в базу данных'

    def import_data(self, model, file_path):
        """Функция загрузки CSV-файла и сохрания в базу данных."""
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            print(reader)

            relation_keys = [
                'category',
                'genre',
                'author',
                'title_id',
                'genre_id',
                'review_id']

            model_instance = []
            for row in reader:
                print(row)                
                for key in relation_keys:
                    print(key)
                    if key in row:
                        print(key)
                        relation_id = row.get(key)
                        print(relation_id)
                        relation_instance = getattr(
                            model, key).relation_instance
                        row[key] = relation_instance.objects.get(
                            pk=relation_id)
                model_instance.append(model(**row))
            model.objects.bulk_create(model_instance)

    def handle(self, *args, **options):
        model_path = {
            Category: 'static/data/category.csv',
            Title: 'static/data/titles.csv',
            Comment: 'static/data/comments.csv',
            Review: 'static/data/review.csv',
            Genre: 'static/data/genre.csv',
            User: 'static/data/users.csv'}
            # Title: 'static/data/genre_title.csv'}
 
        for model, file_path in model_path.items():
            self.import_data(model, file_path)
            self.stdout.write(self.style.SUCCESS(
                f'Данные из {file_path} успешно загружены'))
