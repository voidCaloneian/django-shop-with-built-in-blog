# Generated by Django 4.1.2 on 2022-10-31 12:48

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=False, quality=100, scale=None, size=[510, 510], upload_to='shop/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='reviews_amount',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='Количество отзывов'),
        ),
    ]
