#  Django модули
from django.template import Library
#  Модули проекта
from blogApp.models import Article


register = Library()

@register.simple_tag
def show():
    "Функция получения последних по дате публикации трёх статей"
    last_three_articles = Article.objects.all().order_by('id').reverse()[:3]
    return last_three_articles