# Generated by Django 4.1.2 on 2022-10-27 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0002_alter_article_category_alter_article_preview_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата'),
        ),
    ]