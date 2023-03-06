#  Django модули
from django_resized import ResizedImageField
from django.db import models

#  Модуль расширенного текствого редактора
from ckeditor.fields import RichTextField

import datetime
# Create your models here.

class Article(models.Model):
    "Модель статьи"
    title         = models.CharField('Заголовок', max_length = 70)
    description   = models.CharField('Краткое описание', max_length = 58)
    preview_image = ResizedImageField(size=[370, 266], 
                                      crop=['middle', 'center'], 
                                      upload_to = '%Y/%m/%d/', 
                                      keep_meta = False, 
                                      quality=100,  
                                      blank=False)
    content = RichTextField(blank=False, null=False)
    tags    = models.CharField('Тэги', max_length = 300)
    date    = models.DateField('Дата', default = datetime.date.today) 
    # Выборы для модели category 
    CHOICES = (
        ('Еда', 'Еда'),
        ('Красота', 'Красота'),
        ('Стиль жизни', 'Стиль жизни'),
        ('Путешествия', 'Путешествия')
    )
    # Сама модель
    category = models.CharField('Категория', 
                                choices=CHOICES,
                                default='Еда', 
                                max_length = 11)
    comments_amount = models.SmallIntegerField('Количество комментариев', default = 0)
    
    def __str__(self):
        return self.title.capitalize()