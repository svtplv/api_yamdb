# Generated by Django 3.2 on 2023-12-03 10:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(code='Некорректное имя', message='Имя пользователя должно состоять из букв/цифр/символов @.+-_', regex='^[\\w.@+-]+\\Z')], verbose_name='Имя пользователя'),
        ),
    ]
