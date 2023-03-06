#  django модули
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.views import View

#  Модули из проекта
from .other_modules.searcher import search
from .forms import ArticleForm
from .models import Article

#  template_name - стандартный путь для большинства шаблонов проекта
from basics import template_name

class Params:
    "Класс request Параметров"
    @staticmethod
    def get(data):
        "Функция получения нужных данных из запроса"
        #  Получаем параметры из запроса
        page = data.get('page', 1)
        category = data.get('category', 'Все')
        search = data.get('search', '...')
        
        return category, page, search

class BlogPaginator:
    "Класс пагинатора для блога"
    #  Параметры пагинатора
    def __init__(self, category, search):
        self.category = category
        self.search = search
        self.make_paginator()
    #  Создание пагинатора
    def make_paginator(self):
        "Функция создания пагинатора"
        # Если есть параметр search, получаем список статей через функцию search
        if self.search != '...':
            self.articles = search(self.search)
         # Если категория 'Все', получаем список всех статей
        elif self.category == 'Все':
            self.articles = Article.objects.all().order_by('id')
        #  Иначе получаем список статей только с заданной категорией
        else:
            self.articles = Article.objects.filter(category=self.category).order_by('id')
        self.paginator = Paginator(self.articles, 6)
        
    def get_current_page(self, page):
        "Функция получения пагинатора заданной страницы"
        return self.paginator.page(page)
    
    def get_last_page_number(self) -> int:
        "Функция получения количества страниц в пагинаторе"
        return self.paginator.num_pages

class Blog(View):
    " Класс отвечающий за отображение лога "
    def get(self, request) -> render:
        context = dict()
        # Получаем параметры
        category, page, search = Params.get(request.GET)
        # Создаем экземпляр класса BlogPaginator
        blog_paginator = BlogPaginator(category, search)
        
        # Если идёт поиск
        if search != '...':
            context['searchParams'] = f'search={search}'
            context['orange_row'] = 'Номер страницы: {}<br>Ищем: {}'.format(page, search)
        # Если валидация вернула другой результат, считаем что это категория
        else:
            context['orange_row'] = 'Номер страницы: {}<br>Категория: {}'.format(page, category)
            context['searchParams'] = f'category={category}'

        # Получаем текущую страницу и количество страниц
        current_page = blog_paginator.get_current_page(page)
        last_page_number = blog_paginator.get_last_page_number()

        # Добавляем данные в контекст
        context.update({
            'last_page_number': last_page_number,
            'searchParams': category if not None else search,
            'current_page': current_page,
            'Articles': current_page.object_list,
            'orange_title': 'Статьи',
            'orange_safe': True,
            'path': 'blog'
        })
        
        return render(request, template_name, context)

class ArticleCreation(View):
    "Класс отвечающий за создание статьи"
    ID_PARAM_NAME = 'id'
    
    def get(self, request):
        "Отображение формы для создания статьи"
        return render(request, template_name, {
            'form': ArticleForm(),
            'path': 'blog_creation'
        })

    def post(self, request):
        "Обработка отправки формы для создания статьи"
        form_data = ArticleForm(request.POST, request.FILES)
        if form_data.is_valid():
            try:
                article_id = self.__create_article(data=form_data.cleaned_data)
            except Exception:
                return HttpResponse('Ошибка создания статьи', status=500)
            
            url = reverse('blog') + f'article/?{self.ID_PARAM_NAME}={article_id}'
            return HttpResponseRedirect(url)
        
        errors = form_data.errors.as_text()
        return HttpResponse(errors, status=400)
    
    def __create_article(self, data):
        "Создание статьи на основе данных формы"
        article = Article.objects.create(
            preview_image=data['preview_image'],
            description=data['description'].lower(),
            category=data['category'],
            content=data['content'],
            title=data['title'].lower(),
            tags=data['tags'].lower()
        )
        
        return article.id

class ArticleViewer(View):
    " Класс отвечающий за показ шаблона статьи"
    def get(self, request):
        article_id = request.GET.get('id', None)
        article    = Article.objects.get(id = article_id)
        
        context = {
            'Article' : article,
            'orange_title' : article.title,
            'orange_row'   : article.date,
            'orange_safe'  : False,
            'path' : 'blog_details'
        }
        
        return render(request, template_name, context)