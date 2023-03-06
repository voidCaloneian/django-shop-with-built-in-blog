# Generated by Django 4.1.2 on 2022-10-27 14:31

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('Еда', 'Еда'), ('Красота', 'Красота'), ('Стиль жизни', 'Стиль жизни'), ('Путешествия', 'Путешествия')], default='Еда', max_length=11, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='article',
            name='preview_image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=False, quality=100, scale=None, size=[370, 266], upload_to='%Y/%m/%d/'),
        ),
    ]