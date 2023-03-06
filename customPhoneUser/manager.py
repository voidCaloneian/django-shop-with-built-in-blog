from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер пользователя, где номер 
    телефона - уникальный идентификатор для авторизации
    """
    def create_user(self, phone_number, **extra_fields) -> object:
        """
        Создание пользователя с помощью номера телефона 
        Пароль в админке у всех пользователей - q0w0e=1-2-3
        """
        #  Если номер телефона не указан, то вызываем ошибку
        if not phone_number:
            raise ValueError('Для создания пользователя требуется номер телеофна')
        
        #  Создание пользователя 
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password('q0w0e=1-2-3')  #  На время установил такой пароль
        user.save()
        return user


    def create_superuser(self, phone_number, **extra_fields):
        "Функция создания пользователя с правами администратора в админ панели"
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, **extra_fields)