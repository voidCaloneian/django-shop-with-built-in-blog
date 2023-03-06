#  Django модули
from django.contrib.auth.backends import BaseBackend

#  Модули проекта
from .models import PhoneUser

class SettingsBackend(BaseBackend):
    "Бэкенд авторизации PhoneUser модели"
    def authenticate(self, phone_number=None, password=None):
        "Авторизация по номеру телефона"
        if phone_number:
            try:
                user = PhoneUser.objects.get(phone_number=phone_number)
                return user
            except PhoneUser.DoesNotExist:
                raise(PhoneUser.DoesNotExist)
        return None

    def get_user(self, user_id):
        "Метод получения пользователя"
        try:
            return PhoneUser.objects.get(pk=user_id)
        except PhoneUser.DoesNotExist:
            return None