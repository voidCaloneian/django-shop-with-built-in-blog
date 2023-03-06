#  Django модули
from django import forms

#  Модули проекта
from .models import Article

class ArticleForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs=
                            {'placeholder' : 'Заголовок',
                             'class'       : 'formInput'}))
    description = forms.CharField(widget=forms.TextInput(attrs=
                            {'placeholder' : 'Краткое описание',
                             'class'       : 'formInput'}))
    tags        = forms.CharField(widget=forms.TextInput(attrs=
                            {'placeholder' : 'Тэг1, тэг2, тэг3...',
                             'class'       : 'formInput'}))
    preview_image = forms.ImageField(widget=forms.FileInput(attrs=
                            {'class' : 'primary-btn primary-btn-added preview_image_class'}))
    
    class Meta:
        model  = Article
        fields = ('title', 
                  'description',
                  'preview_image',
                  'content',
                  'tags',
                  'category')