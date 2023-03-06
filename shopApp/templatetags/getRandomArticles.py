from django.template import Library
from blogApp.models import Article
from random import sample

register = Library()

@register.simple_tag
def getRandomArticles():
    
    articles = list(Article.objects.all())
    if articles:
        randomed_articles = sample(articles, k=3)
        return randomed_articles
    else:
        return None
    