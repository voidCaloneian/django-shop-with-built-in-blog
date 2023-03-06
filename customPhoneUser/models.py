#  Django модули
from django.contrib.auth.models import AbstractUser
from django.db import models

# Модули проекта
from .manager import CustomUserManager


class PhoneUser(AbstractUser):
    "Текущий класс пользователя проекта, также используется в админке"
    username = None
    phone_number = models.CharField('Номер телефона', unique=True, max_length=11)

    #  Обозначение, что кастомное phone_number поле 
    #  заменяет стандартное username поле 
    USERNAME_FIELD = 'phone_number'
    #  Определение обязательных полей является пустым
    #  Чтобы необязательно было вводить пароль при регистрации и авторизации
    REQUIRED_FIELDS = []

    #  Управление методом objects
    #  передаётся кастомному менеджеру проекта
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number