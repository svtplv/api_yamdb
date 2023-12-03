import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reviews.models import Title, Genre, Category, Review, Comment

User = get_user_model()

class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов в базу данных'

    def import_data(self, model, file_path):
        """Функция загрузки CSV-файла и сохранения в базе данных."""
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            model_instance = []
            for row in reader:
                row['id'] = int(row['id'])
                
                # Проверка наличия поля 'category'
                if 'category' in row:
                    row['category'] = Category.objects.get(
                        id=int(row['category']))

                # Проверка наличия поля 'author'
                if 'author' in row:
                    user_id = int(row['author'])
                    if User.objects.filter(id=user_id).exists():
                        row['author'] = User.objects.get(id=user_id)
                    else:
                        self.stdout.write(self.style.SUCCESS(
                            f'User с таким id={user_id} не найден.'))
               
                if model == Comment:
                    # Обязательное поле title_id для Comment
                    title_id = int(row['title_id'])
                    if Title.objects.filter(id=title_id).exists():
                        row['title_id'] = Title.objects.get(id=title_id)
                    else:
                        self.stdout.write(self.style.SUCCESS(
                            f'Title c таким id={title_id} не найден'))
                model_instance.append(model(**row))
            model.objects.bulk_create(model_instance)

    def handle(self, *args, **options):
        model_path = {
            User: 'static/data/users.csv',
            Category: 'static/data/category.csv',
            Title: 'static/data/titles.csv',
            Comment: 'static/data/comments.csv',
            Review: 'static/data/review.csv',
            Genre: 'static/data/genre.csv'
            # Title: 'static/data/genre_title.csv'
        }

        for model, file_path in model_path.items():
            self.import_data(model, file_path)
            self.stdout.write(self.style.SUCCESS(
                f'Данные из {file_path} успешно загружены'))
