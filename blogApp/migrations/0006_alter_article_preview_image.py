# Generated by Django 4.1.3 on 2022-12-18 03:40

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0005_alter_article_preview_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='preview_image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=False, quality=100, scale=None, size=[370, 266], upload_to='%Y/%m/%d/'),
        ),
    ]
