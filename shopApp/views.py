#  Django модули
from django.template.loader import render_to_string
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.db.models import F, Min, Max
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

#  Модули проекта
from .models import Product, PriceRange
from basics import template_name


class Params:
    " Класс для обработки параметров запроса "
    @staticmethod
    def unpackedParams(request):
        " Метод для распаковки строки параметров из куки "
        #  Получаем строку параметров из куки
        string = request.COOKIES.get('params')
        #  Если строка параметров пустая, то формируем ее из GET запроса
        if string == None or len(string) == 0: 
            string = '?category={}&ordering=Алфавит'.format(
                request.GET.get('category')
            )
            
        #  Разбиваем строку параметров на словарь
        splitted = string[1:].split('&')
        params = {el[0] : el[1] for el in [param.split('=') for param in splitted]}
        
        if params['category'] == 'мы нашли:' and not request.GET.get('search'):
            params['category'] = 'акции'
        
        #  Если не указаны минимальная и максимальная цена, то берем их из БД
        if params.get('min_price') in ('NaN', None):
            if params['category'] in ('None', None, ''):
                category_from_request = request.GET.get('category')
                
                if category_from_request != None:
                    params['category'] = category_from_request
                else:
                    params['category'] = 'акции'
            

            category_prices = PriceRange.objects.get(category__name=params['category'])
            
            params['min_price'] = category_prices.min_price
            params['max_price'] = category_prices.max_price
            
        
        #  Возвращаем распакованный словарь параметров
        return params
    
    @staticmethod
    def get(request) -> tuple[str, str, int, int, int]:
        "Функция получения нужных параметров из запроса"
        data = Params.unpackedParams(request)
        #  Получаем категорию, если не удалось, тогда устанавливаем значение - 'акции'
        category = data.get('category', 'акции')
        #  Получаем метод сортировки
        ordering = data.get('ordering', 'Алфавит')
        #  Получаем минимальную и максимальную цену слайдера цены
        min_price = int(data.get('min_price', 0))
        max_price = int(data.get('max_price', 999999999)) 
        # Получаем номер текущей страницы, если не удалось, тогда устанавливаем значение - 1
        page = int(request.COOKIES.get('page', 1))
        return category, ordering, min_price, max_price, page
        
class Pagination:
    "Класс пагинации магазина"
    def __init__(self, products: list[Product], page: int, per_page: int = 9):
        "Объявление параметров пагинатора"
        self.products = products
        self.paginator = Paginator(products, per_page)
        self.page = self.paginator.page(page)
        
    def get_products_on_current_page(self):
        "Получение списка продуктов текущей страницы"
        return self.page.object_list

    def get_rendered_products(self):
        "Получение продуктов отрендеренных в html код"
        products = render_to_string(
            template_name='shop/shop_grid/components/products_block/products.html',
            context={
                'products' : self.page.object_list
            },
        )
        return products, len(self.page.paginator.object_list)

    def get_rendered_pagination(self, search_words = None):
        "Получение пагинации отрендеренной в html код"
        pagination = render_to_string(
            template_name='shop/shop_grid/components/pagination.html',
            context={
                'current_page' : self.page,
                'last_page_number' : self.paginator.num_pages,
                'search_words' : search_words
            }
        )
        return pagination
    
    def get_current_page_pagination(self):
        "Получение пагинации текущей страницы"
        return self.page
    
    @staticmethod
    def request_is_ajax(request) -> bool:
        "Функция проверяет, является ли запрос - ajax-запросом"
        # Проверяем заголовок 'X-Requested-With' в запросе.
        # Если он равен 'XMLHttpRequest', то запрос является AJAX-запросом.
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return True
        else: return False
    
    def response_to_ajax(self, search_words = None) -> JsonResponse:
        "Функция ответа ajax-запросу"
        #  Получаем отрендеренные блоки HTML кода продуктов и пагинации
        products, products_amount = self.get_rendered_products()
        pagination = self.get_rendered_pagination(search_words=search_words)
        #  Формируем JSON ответ
        json = {
            'products'        : products,
            'pagination'      : pagination,
            'products_amount' : products_amount
        }
        return JsonResponse(
            data=json,
            safe=False
        )

class Shop(View):
    "Класс магазина"
    
    ORDER_BY = {
    'Алфавит' : ('name',),
    'Скидка'  : ('-discount__discount_value', '-discount__discounted_price', '-price')
    }
    
    def get(self, request):
        #  Если в запросе присутствует параметр "search", то вызываем
        #  Направляем запрос в класс поиска
        if request.GET.get('search'):
            return Search().get(request)
        #  Получение параметров из запроса
        category, ordering, min_price, max_price, page = Params.get(request)
        #  Получение отсортированных и упорядоченных продуктов по параметрам
        products = self.get_ordered_products(category, ordering, min_price, max_price)
        #  Получение пагинации с текущими продуктами и страницей
        pagination = Pagination(products, page)
        #  Проверяем, является ли запрос - ajax-запросом, если да,
        #  То отправляем ответ серверу с продуктами и пагинацией
        if pagination.request_is_ajax(request):
            return pagination.response_to_ajax()
        #  Если нет, то рендерим страницу
        else:
            #  Получаем минимальную и максимальную цену выбранной категории
            #  Для установки соответсвующих значений в слайдер цены
            try:
                category_range = PriceRange.objects.get(category__name=category)
            #  В определенных случаях категория не определенна
            #  Для этого случая категория = 'акции" 
            except PriceRange.DoesNotExist:
                category_range = PriceRange.objects.get(category__name='акции')
                
            context = {
                'path': 'shop',
                'products': pagination.get_products_on_current_page(),
                'min_price': category_range.min_price,
                'max_price': category_range.max_price,
                'CATEGORY': category,
                'current_page': pagination.get_current_page_pagination(),
                'products_found': len(products),
                'last_page_number' : pagination.paginator.num_pages
            }
            return render(request, template_name, context)

    def get_ordered_products(self, category, ordering, min_price, max_price, search_words = None):
        "Функция получения отсортированных по параметрам продуктов"
        #  Если идёт упорядочивание по цене
        if ordering in ('Цена to-low', 'Цена to-high'):
            products = self.get_price_ordered_products(category, min_price, max_price, search_words=search_words)
            if ordering == 'Цена to-high':
                products = products.order_by('final_price')
            else:
                products = products.order_by('-final_price')
        #  Если по алфавиту, либо размеру скидки
        else:
            products = self.get_alphabetically_or_discount_ordered_products(
                category, min_price, max_price, search_words=search_words
            )
            products = products.order_by(*self.ORDER_BY[ordering])
        return products

    def get_products_by_category(self, category, search_words = None):
        "Получение продуктов соответствующей категории"
        #  Если идёт поиск
        if category == 'поиск':
            return Search.search_product_by_name(search_words=search_words)
        #  Если категория - акции
        elif category == 'акции':
            return Product.objects.exclude(discount=None)
        #  Во всех остальных случаях (Стандартные категории)
        return Product.objects.filter(category__name=category)
    
    def get_price_ordered_products(self, category, min_price, max_price, search_words = None):
        "Упорядочивает продукты и возвращает их QuerySet"
        products = self.get_products_by_category(category, search_words=search_words)
        #  final_price берет за цену товара цену товара со скидкой, если она есть
        #  Либо просто цену товара, если скидок на него никаких нет
        #  После этого фильтрует продукты по ценовому диапозону
        products = products.select_related('discount').annotate(
            final_price=Coalesce(F('discount__discounted_price'), F('price'))
        ).filter(
            final_price__gte=min_price,
            final_price__lte=max_price
        )
        return products

    def get_alphabetically_or_discount_ordered_products(self, category, min_price, max_price, search_words = None):
        "Упорядочивает продукты по алфавиту, либо по размеру скидки"
        products = self.get_products_by_category(category, search_words=search_words)
        #  final_price берет за цену товара цену товара со скидкой, если она есть
        #  Либо просто цену товара, если скидок на него никаких нет
        #  После этого фильтрует продукты по ценовому диапозону
        products = products.select_related('discount').annotate(
            final_price=Coalesce(F('discount__discounted_price'), F('price'))
        ).filter(
            final_price__gte=min_price,
            final_price__lte=max_price
        )
        return products
    
class Search(View):
    "Класс поиска по продуктам"
    def get(self, request):
        """
        Возвращает отрендеренную страницу продуктов, 
        либо блок продуктов с пагинацей
        в случае, если запрос - ajax-запрос
        """
        #  Получение продуктов текущего запроса
        search_words, ordering, min_price, max_price, page = self.getRequestParams(request.GET, request.COOKIES) 
        #  Получение отсортированных и упорядоченных продуктов по параметрам
        products = Shop().get_ordered_products('поиск', ordering, min_price, max_price, search_words=search_words)
        #  Получение минимальной и максимальной цены продуктов, которые подошли по параметрам
        products_min_and_max_prices = products.annotate(
        final_price=Coalesce(F('discount__discounted_price'), F('price'))
            ).aggregate(
                min_price=Min('final_price'), max_price=Max('final_price')
        )
        #  Переменные со стандартными значениями цен.
        #  Нужны в случае, если min_price и max_price запроса не были объявлены
        default_min_price = products_min_and_max_prices['min_price']
        default_max_price = products_min_and_max_prices['max_price']
        pagination = Pagination(products, page)
        
        #  Если текущий запрос - ajax-запрос, то отправляем ему ответ
        #  С отрендеренными пагинацией и продуктами
        if pagination.request_is_ajax(request):
            return pagination.response_to_ajax(search_words=search_words)
            
        context = {
            'path' : 'shop',
            'products' : pagination.get_products_on_current_page(),
            'min_price' : min_price if min_price > 0 else default_min_price,
            'max_price' : max_price if max_price < 999999 else default_max_price,
            'current_page' : pagination.get_current_page_pagination(),
            'last_page_number' : 1,
            'products_found' : len(products),
            'CATEGORY' : 'Мы нашли:',
            'search' : search_words
        }
        return render(request, template_name, context)    
    
    @staticmethod
    def getRequestParams(data, cookies) -> list[str, str, int, int, int]:
        "Получение параметров запроса"
        search_words = data.get('search').strip().lower()
        min_price = int(data.get('min_price', 0))
        max_price = int(data.get('max_price', 999999))
        ordering = data.get('ordering', 'Алфавит')
        
        #  Получение параметра 'page' из куки
        #  В случае, если len(page) < 1, что означает
        #  то, что параметр пустой, получаем GET параметр из 
        #  запроса, если и его нет, то page = 1
        page = cookies.get('page')
        if len(page) < 1:
            page = data.get('page', 1)
        page = int(page)
        
        return search_words, ordering, min_price, max_price, page
    
    @staticmethod
    def search_product_by_name(search_words):
        "Поиск подходящих по имени продуктов"
        #  Получаем список всех продуктов
        products = Product.objects.all()
        #  Получаем только те продукты, имена которых содержат наши слова поиска.
        filtered_names = (product.name for product in products if search_words in product.name.lower())
        filtered_products = products.filter(name__in=filtered_names)
        #  Не использовал name__icontains, так как нужна текущая кодировка
        #  базы данных не позволяет искать символы кириллицы
        return filtered_products
    