#  Django модули
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

#  Модули проекта
from shopApp.models import *
from shopApp.models import Promo
from basics import template_name

class Details(View):
    "Класс для отображения страницы с подробной информацией о товаре"
    def get(self, request):
        #  Получаем идентификатор товара из GET-параметров
        product_id = int(request.GET.get('id', None))
        #  Получаем объект товара из базы данных
        product = Product.objects.get(id=product_id)
        #  Проверяем, есть ли товар в корзине пользователя
        product_in_shopping_cart = check_if_product_in_shopping_cart(request.COOKIES, product_id)
        #  Формируем контекст для шаблона
        context = {
            'product' : product,
            'product_in_shopping_cart' : product_in_shopping_cart,
            'path' : 'details',
            'reviews' : Reviews.get_reviews_for_product(product, request.user),
            'current_user_review' : Reviews.get_current_user_review(user=request.user, product=product),
            'reviews_amount' : product.count_reviews()
        }
        
        return render(request, template_name, context)
    
class Reviews(View):
    "Класс отзыва товара"
    @staticmethod
    def get_current_user_review(user, product) -> Review | None:
        "Получение отзыва текущего пользователя запроса на текущий продукт запроса"
        #  Если юзер не авторизован, то ничего не возвращаем
        if user.is_authenticated:
            try:
                return Review.objects.get(author=user, product=product)
            except Review.DoesNotExist:
                return None
        return None
    
    @staticmethod
    def get_reviews_for_product(product, user, amount = 4, ):
        "Получение четырех отзывов для текущего продукта"
        #  Если пользователь авторизован, то 
        #  берем все отзывы продукта, кроме отзыва самого пользователя
        if user.is_authenticated:
            last_four_review = product.reviews.exclude(author=user).order_by('-created_at')[:amount]
        else:
            last_four_review = product.reviews.order_by('-created_at')[:amount]
        return last_four_review
        
    @staticmethod
    def have_more_review(last_review_index, product_id):
        "Проверка, есть ли у продукта ещё отзывы"
        #  last_review_index - параметр ajax-запроса, 
        #  отвечающий за индекс последнего присланного индекса отзыва
        if last_review_index > Review.objects.filter(product__id=product_id).count():
            return False
        else: 
            return True
    
    @staticmethod
    def get_other_four_review(request):
        "Получение еще четырех отзывов"
        #  Получение данных из запроса
        data = request.GET
        last_review_index = int(data.get('last_review_index', 4))
        product_id = data.get('product_id')
        
        user = request.user
        #  Если пользователь не авторизован, то
        #  Делаем его 'None', чтобы запрос прошёл
        if not user.is_authenticated: user = None 
        #  Если есть ещё отзывы у товара, то возвращаем их
        if Reviews.have_more_review(last_review_index, product_id):
            other_four_review = Review.objects.filter(
                product__id=product_id
            ).exclude(
                author=user
            ).order_by('-created_at')[last_review_index:last_review_index + 4]
            
            rendered_four_review = render_to_string(
                'shopping/shop_details/components/reviews.html', {
                    'new_reviews' : other_four_review,
                    'adding_new' : True,
                    }
            )
            
            json = {'reviews' : rendered_four_review}
            
            return JsonResponse(
                json,
                safe=False
            )
        #  Иначе возвращаем ошибку
        else:
            return HttpResponse(status=400)
    
    def post(self, request):
        "Функция публикации отзыва"
        #  Получаем данные из запроса
        data = request.POST
        product_id = data.get('product_id')
        comment = data.get('review')
        rating = data.get('rating')
        
        #  Ошибка возникает в случае, 
        #  если отзыв от текущего пользователя у текущего товара уже оставлен
        try:
            Review(
                product_id=product_id,
                rating=rating,
                comment=comment,
                author=request.user
            ).save()
            return HttpResponse(status=200)
        except ValueError:
            return HttpResponse(status=400)

class ShoppingCart(View):
    "Класс визуального отображения корзины"
    def get(self, request):
        #  Формируем контекст для шаблона
        context = {'path' : 'cart'}
        #  Получаем список идентификаторов товаров из куки
        product_ids = request.COOKIES.get('product_ids', None)
        products = None
        
        if product_ids:
            #  Разделяем строку с идентификаторами на отдельные идентификаторы,
            #  извлекаем из них числовые значения и помещаем их в список
            product_ids = [_id for _id in [item.split('_')[0] for item in product_ids.split(' ')]]
            #  Получаем объекты товаров из базы данных по списку идентификаторов
            products = tuple(Product.objects.in_bulk(product_ids).values())
            
        context['products'] = products if products else None
        return render(request, template_name, context) 

def get_shopping_cart_total_price(request):
    "Функция подсчёта суммарной стоимости корзины"
    #  Получаем словарь продуктов и их количества из объекта request
    products = dict(request.GET)
    products_amount = {a:int(products[a][0]) for a in products}
    #  Проверяем, есть ли информация о продуктах в словаре
    if products_amount:
        #  Получаем цены, идентификаторы и количество продуктов
        product_qs = Product.objects.filter(
            id__in=products_amount
        ).values('id', 'discount__discounted_price', 'price')
        #  Вычисляем общую стоимость
        total_price = 0
        for product_price in product_qs:
            if product_price['discount__discounted_price']:
                product_total_price  = product_price['discount__discounted_price'] \
                    * int(products_amount[str(product_price['id'])])
            else:
                product_total_price = product_price['price'] \
                    * int(products_amount[str(product_price['id'])])
            total_price+= product_total_price
            
        #  Возвращаем ответ, содержащий общую стоимость
        return JsonResponse({'total_price' : total_price})
    else: 
        # Если информации о продуктах нет, возвращаем ответ со значением 0
        return JsonResponse({'total_price' : 0})
    
def promoUsage(request):
    "Функция использования промокода на странице корзины"
    try:
        promo = Promo.objects.get(code = request.GET.get('promo', None).upper())
        #  Если промокод найден, то отправляем размер его скидки и его описание
        return JsonResponse({'discount' : promo.discount, 'description' : promo.description})
    except Promo.DoesNotExist:
        return HttpResponse(status=400)
    
def check_if_product_in_shopping_cart(cookies, product_id):
    "Функция проверки, находится ли товар в корзине"
    #  Получаем список идентификаторов товаров из куки
    product_ids_and_amounts = cookies.get('product_ids', None)
    
    if product_ids_and_amounts:
        product_ids = [int(_id.split('_')[0]) for _id in product_ids_and_amounts.split(' ')]
        #  Проверяем, есть ли продукт в нашем продукт листе
        if product_ids:
            return product_id in product_ids
    else:
        return False