#  Django модули
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Avg
from django.db import models

#  Модули проекта
from customPhoneUser.models import PhoneUser


class Category(models.Model):
    "Класс категории продуктов"
    name = models.CharField('Категория', max_length=40)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    "Класс продукта магазина"
    price = models.SmallIntegerField('Цена', validators=[MinValueValidator(1)])
    category = models.ForeignKey(Category, on_delete=models.PROTECT)      
    
    amount = models.PositiveSmallIntegerField('Количество')
    name  = models.CharField('Название', max_length = 90)
    rating = models.PositiveSmallIntegerField('Оценка', default = 0, blank=True)
    weight = models.PositiveSmallIntegerField('Вес')
    discount = models.OneToOneField('Discounts', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Акция')
    image = models.ImageField('Картинка', blank=True, upload_to='shop/')
    
    def count_reviews(self):
        "Подсчитать количество отзывов у текущего продукта"
        return self.reviews.all().count()
    
    def average_review_rating(self):
        "Подсчитать среднее арифмитиечское рейтинга отзыов у текущего продукта"
        try:
            return round(self.reviews.aggregate(Avg('rating'))['rating__avg'], 2)
        except TypeError:
            return 'Нет отзывов'
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['category']
   
class Review(models.Model):
    "Класс отзыва продукта магазина"
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='reviews')
    rating = models.SmallIntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField('Сам отзыв', max_length=450)
    
    author = models.ForeignKey(PhoneUser, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    def is_unique(self):
        "Проверка на то, оставлял ли текущий пользователь отзывы на выбранный товар"
        # Проверяем, что пользователь еще не оставлял отзыв на этот товар
        if Review.objects.filter(author=self.author, product=self.product).exists():
            return False
        return True
    
    def save(self, *args, **kwargs):
        "Кастомный сейв для проверки на уникальность отзыва"
        # проверяем уникальность отзыва перед сохранением
        if not self.is_unique():
            raise ValueError('Вы уже оставляли отзыв на этот товар')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.author} : {self.product.name}'
    
class PriceRange(models.Model):
    "Класс диапозона цен магазина для каждой категории"
    category  = models.OneToOneField(Category, on_delete=models.CASCADE) 
    min_price = models.PositiveSmallIntegerField('Минимальная цена', default=9999999)
    max_price = models.PositiveSmallIntegerField('Максимальная цена', default=0)
    
    def __str__(self):
        return self.category.name
    
class Discounts(models.Model):
    "Класс скидки продукта магазина"
    rel_product = models.OneToOneField(Product, on_delete = models.CASCADE, verbose_name='Продукт')
    discount_value = models.PositiveSmallIntegerField('Размер скидки', validators=[MinValueValidator(1), MaxValueValidator(99)])
    discounted_price = models.PositiveSmallIntegerField('Цена со скидкой', blank=True, default = 0, editable=False)
    
    @staticmethod
    def discount_price(price : int, discount_value : int) -> int:
        "Получение цены продукта со скидкой"
        return int(price * ((100 - discount_value) / 100) // 1)
    
    def __str__(self):
        return self.rel_product.name
    
    class Meta:
        ordering = ['rel_product__name']
        

class Promo(models.Model):
    "Класс промокода магазина"
    code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveSmallIntegerField('Размер скидки', validators=[MinValueValidator(1), MaxValueValidator(100)])
    expiration_date = models.DateTimeField('Дата окончания действия промокода', default=timezone.now) #  По стандарту промокод имеет истекший период действия
    max_uses = models.IntegerField('Максимальное количество использований', default=1)
    used = models.IntegerField('Коилчество использований', default=0)
    is_active = models.BooleanField('Активен?', default=True)
    description = models.TextField('Описание', blank=True)
    
    def __str__(self):
        return '{} : {}'.format(
            self.code, self.description[:50]
        )

#########################################################
#                  Функции Сигналов                     #
#########################################################

def aggregate_actioned_prices():
    """
    Получение минимальной и максимальной цены со скидкой. 
    Функция предназначена для сигнала по установке диапозона цен на категорию 'акции'
    """
    discounts = [ a['discounted_price'] for a in Discounts.objects.all().values('discounted_price') ]
    # Проверка на случай того, что ВСЕ скидки удалены
    if discounts:
        return min(discounts), max(discounts)
    else: return 0, 0
    
def UpdatePriceRange(category: Category.id) -> None:
    "Обновление цен выбранной категории"
    category_for_update = PriceRange.objects.filter(category=category)  
    
    if category == 10:
        min_price, max_price = aggregate_actioned_prices()                          
    else: min_price, max_price = aggregate_prices(category)    
    
    category_for_update.update(min_price=min_price, max_price=max_price)    
    
def aggregate_prices(category : Category) -> tuple:
    "Получение минимальной и максимальной цен"
    products = Product.objects.filter(category=category).values(
        'discount__discounted_price',
        'price'
    )
    
    #  Если у категории нет продуктов, то выставляем нули
    if not products:
        return 0, 0
    price_list = [obj['discount__discounted_price'] or obj['price'] for obj in products]
    
    return min(price_list), max(price_list)

def linkDiscount(instance):
    """
    Функция мгновенной связки продукта со скидкой 
    для учёта цены со скидкой, пока запись ещё 
    не была добавлена в базу данных
    """
    product = Product.objects.get(id=instance.rel_product.id)
    #  Связываем скидку с товаром
    product.discount_id = instance.id
    product.save()
    
def refreshDiscountedPrice(instance):
    "Обновление цены со сидкой, также до добавления в бд"
    discount = Discounts.objects.filter(id = instance.id)
    #  Обновляем цену со скидкой
    discount.update(
        discounted_price = instance.discount_price(
            instance.rel_product.price,
            instance.discount_value
        )
    )
    
def refreshDiscountedPriceByProduct(instance):
    "Обновление цены со скидкой продукту"
    if instance.discount:
        related_discount_query = Discounts.objects.filter(id = instance.discount.id)
        related_discount = related_discount_query[0]
        related_discount_query.update(
            discounted_price=related_discount.discount_price(
                related_discount.rel_product.price,
                related_discount.discount_value
            )
        )
    UpdatePriceRange(
        category=instance.category_id,
    )
    
def deleteProduct_s_Discount(instance):
    "Удаление скидок у продуктов до внесения в базу данных"
    related_product = Product.objects.filter(id = instance.rel_product.id)
    related_product.update(discount = None)
    
#########################################################
#                       СИГНАЛЫ                         #
#########################################################
@receiver(post_save, sender=Discounts)
def save_signal_receiver(sender, instance, **kwargs):
    "После добавления скидки обновляем диапозон цен"
    #   Если скидка только что была создана, то
    #         Продукт с ней линкуется
    if kwargs['created']: linkDiscount(instance)
    
    #   Если меняется размер скидки (self.discount_value)
    # То по формуле вычисляется цена с учетом новой скидки
    refreshDiscountedPrice(instance)
    
    # Обновляется разброс цен
    UpdatePriceRange(category=instance.rel_product.category_id)
    UpdatePriceRange(category=10) # Категория 'акции'
    
@receiver(post_delete, sender=Discounts)
def delete_signal_receiver(sender, instance, **kwargs):
    "После удаления скидки обновляем диапозон цен"
    UpdatePriceRange(category=instance.rel_product.category_id)
    UpdatePriceRange(category=10) # Категория 'акции'
    deleteProduct_s_Discount(instance)
    
@receiver(post_save, sender=Product)
def save_signal_receiver(sender, instance, **kwargs):
    "После сохранения продукта обновляем общую продукта"
    # Обновляем цену по значению "размер скидки"
    refreshDiscountedPriceByProduct(instance)
    
@receiver(post_delete, sender=Product)
def delete_signal_receiver(sender, instance, **kwargs):
    "После удаления продукта обновляется диапозон цен"
    UpdatePriceRange(category=instance.category_id)