# Generated by Django 4.1.2 on 2022-11-24 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0014_pricerange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricerange',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shopApp.category'),
        ),
    ]
