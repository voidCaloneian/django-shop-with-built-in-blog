# Generated by Django 4.1.3 on 2022-12-18 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0027_alter_discounts_options_alter_pricerange_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=90, verbose_name='Название'),
        ),
    ]
