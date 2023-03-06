from django.template import Library
from shopApp.models import Product
from random import choices

register = Library()

@register.simple_tag 
def getRandomProducts(category_id):
    
    products = Product.objects.filter(category_id = category_id)
    
    randomed_products = choices(products, k=4)
    
    return randomed_products