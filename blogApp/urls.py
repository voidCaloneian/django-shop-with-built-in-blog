#  Django модули
from django.urls import path, re_path

#  Модули проекта
from . import views 

urlpatterns = [
    path('', views.Blog.as_view(), name='blog'),
    path('creation', views.ArticleCreation.as_view()),
    re_path(r'^article/\w*', views.ArticleViewer.as_view()),
    re_path(r'search/\w*', views.Blog.as_view())
] 