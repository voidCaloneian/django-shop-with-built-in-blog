# Generated by Django 4.1.2 on 2022-11-25 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0016_alter_pricerange_min_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_value',
            field=models.PositiveSmallIntegerField(default=0, help_text='Добавить скидку продукту можно в категории "Скидки"', verbose_name='Размер скидки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.PositiveSmallIntegerField(blank=True, default=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Цена'), help_text='Автоматически высчитывается по формуле', null=True, verbose_name='Цена со скидкой'),
        ),
    ]
