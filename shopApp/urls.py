#  Django модули
from django.urls import path
#  Модули проекта
from shoppingApp.views import *
from .views import *


urlpatterns = [
    path('', Shop.as_view(), name='shop'),
    path('search/', Search.as_view(), name='search'),
    path('product/', Details.as_view(), name='product'),
    path('review/', Reviews.as_view(), name ='review'),
    path('review/get_more/', Reviews.get_other_four_review, name='get_more_review'),
    
    path('promo/', promoUsage, name='promo'),
    path('shopping_cart/', ShoppingCart.as_view(), name='shopping_cart'),
    path('shopping_cart_get_total_price/', get_shopping_cart_total_price, name='get_shopping_cart_total_price')
    
]