#  Django модули
from django.contrib import admin
#  Модули проекта
from .models import *

class ProductAdmin(admin.ModelAdmin):
    "Класс отображение продукта в админке"
    model = Product
    
    list_display = ('name', 'price', 'category')
    search_fields = ('name',)
    
    readonly_fields = ('discount', 
                       'get_discount_value', 
                       'get_discounted_price', 
                       'get_reviews_amount', 
                       'get_reviews_rating',
    )
    
    fields = (('name', 'category'), 
              ('price', 'discount', 'get_discount_value', 'get_discounted_price'),
              'weight', 
              'amount',
              ('get_reviews_rating', 'get_reviews_amount'),
              'image'
              )
    
    @admin.display(description='Количество отзывов')
    def get_reviews_amount(self, obj):
        return f'{obj.count_reviews()}'
    
    @admin.display(description='Оценка')
    def get_reviews_rating(self, obj):
        return f'{obj.average_review_rating()}'
    
    @admin.display(description='Размер скидки')
    def get_discount_value(self, obj):
        return f"{obj.discount.discount_value} %"
    
    @admin.display(description='Цена со скидкой')
    def get_discounted_price(self, obj):
        return f"{obj.discount.discounted_price} ₽"
    
admin.site.register(Product, ProductAdmin)

class DiscountsAdmin(admin.ModelAdmin):
    "Класс отображение скидки в админке"
    readonly_fields = ('get_product_price', 'get_product_discounted_price')
    
    # Расположение обновляющего информацию скрипта 
    # shopEnvironment\Lib\site-packages\django\contrib\admin\static\admin\js\shop\adminAjax.js
    
    @admin.display(description='Цена продукта', empty_value='',)
    def get_product_price(self, obj):
        return obj.rel_product.price
    
    @admin.display(description='Цена продукта с учётом скидки')
    def get_product_discounted_price(self, obj):
        return obj.discounted_price
    
admin.site.register(Discounts, DiscountsAdmin)
    
class CategoryAdmin(admin.ModelAdmin):
    "Класс отображение категорий в админке"
    list_display = ('name', 'id')
    
admin.site.register(Category, CategoryAdmin)

class PriceRangeAdmin(admin.ModelAdmin):
    "Класс отображение диапозона цен в админке"
    list_display = ('category', 'min_price', 'max_price')
    
admin.site.register(PriceRange, PriceRangeAdmin)
    
class PromoAdmin(admin.ModelAdmin):
    "Класс отображение промокода в админке"
    readonly_fields = ('used',)
    
admin.site.register(Promo, PromoAdmin)

admin.site.register(Review)
