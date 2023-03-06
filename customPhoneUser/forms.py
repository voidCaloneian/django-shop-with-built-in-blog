#  Django модули
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

#  Модули проекта
from .models import PhoneUser

#  Форма авторизации и регистрации пользователя
class LoginForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        label='Введите номер телефона',
        widget=forms.TextInput(
            attrs={
                'class' : 'phone',
                'autocomplete': 'off',
            }
        )
    )
    
    class Meta:
        model = PhoneUser
        fields = (
            'phone_number',
        )