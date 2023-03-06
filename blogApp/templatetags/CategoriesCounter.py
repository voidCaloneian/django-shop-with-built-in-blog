#  Django модули
from django.template import Library
# Модули проекта
from blogApp.models import Article


register = Library()

@register.simple_tag
def countCategory(category):
    "Функция подсчёта статей определенной категории"
    if category == 'Все':
        return Article.objects.all().count()
    else: 
        return Article.objects.filter(category = category).count()
