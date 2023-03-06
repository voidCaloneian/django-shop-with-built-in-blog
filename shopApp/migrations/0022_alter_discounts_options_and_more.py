# Generated by Django 4.1.3 on 2022-11-29 17:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0021_alter_product_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discounts',
            options={},
        ),
        migrations.AlterField(
            model_name='discounts',
            name='discount_value',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Размер скидки'),
        ),
        migrations.AlterField(
            model_name='discounts',
            name='discounted_price',
            field=models.PositiveSmallIntegerField(blank=True, default=0, editable=False, verbose_name='Цена со скидкой'),
        ),
        migrations.AlterField(
            model_name='discounts',
            name='rel_product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='shopApp.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopApp.discounts', verbose_name='Акция'),
        ),
    ]