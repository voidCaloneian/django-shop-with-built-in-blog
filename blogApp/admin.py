#  Django модули
from django.contrib import admin
#  Модули проекта
from .models import Article


admin.site.register(Article)
