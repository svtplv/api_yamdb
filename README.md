# API YaMDb
## Описание

Проект YaMDb собирает отзывы пользователей на различные произведения. Произведения делятся на категории и жанры. Администраторы добавляют произведения, категории и жанры. Пользователи могут оставлять на эти произведения свои отзывы и проставлять оценки, а также есть возможность комментировать отзывы других пользователей.

### Установка

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:svtplv/api_yamdb.git
```

2. Cоздать и активировать виртуальное окружение:
* Linux/macOS:
```
python3 -m venv venv
source venv/bin/activate
```
* Windows:
```
python -m venv venv
source env/scripts/activate
```

3. Установить зависимости из файла requirements.txt:
pip install -r requirements.txt

4. Выполнить миграции:
```
python3 manage.py migrate
```

5. Запустить проект:
```
python manage.py runserver
```

### Документация

```
http://127.0.0.1:8000/redoc/
```
### Примеры запросов
***Получить список всех категорий:***
```
http://127.0.0.1:8000/api/v1/categories/
```
GET-запрос:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
***Добавить произведение:***
```
http://127.0.0.1:8000/api/v1/titles/
```
POST-запрос:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
### Авторы

[Святослав Поляков](https://github.com/svtplv)
[Ксения Седова](https://github.com/KseniiaSedova)
[Елена Губаева](https://github.com/Lena-001)