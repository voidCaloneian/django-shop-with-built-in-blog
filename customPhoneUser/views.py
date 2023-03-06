#  Django модули
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse, HttpResponse
from django.contrib.auth import login, logout
from django.shortcuts import render

#  Модули текущего проекта 
from .forms import LoginForm
from .backend import * 

#  Модули сторонних библиотек
from random import randint
from re import findall
import redis



#  Соединение с сервером Редиса
redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)


def unmaskNumber(phone_number):
    "Превращает номер вида +7 (999) 999 99 99 в 79999999999"
    return ''.join(findall('\d', phone_number))

def log_in(request):
    "Функция отображение логин шаблона"
    form = LoginForm()
    return render(
        request, 
        'other_templates/login/login.html',
        {'form' : form}
    )
 
def log_out(request):
    "Функция выхода из аккаунта"
    logout(request)
    #  Делаем редирект на последнюю страницу, с которой пользователь нажал 
    #  На кнопку авторизации
    last_page = request.GET.get('last_page', '/shop/?category=акции')
    return HttpResponseRedirect(last_page)

def check_phone_number(request):
    "Функция на проверку, зарегистрирован ли текущий номер телефона"
    #  Проверять, состоит ли номер телефона из 11 цифр не нужно, так как
    #  Идёт проверка ещё перед отправкой ajax-запроса
    phone_number = request.GET.get('phone_number')
    #  Снимаем js маску с номера, чтобы он состоял только из цифр
    phone_number = unmaskNumber(phone_number)
    try:
        PhoneUser.objects.get(
            phone_number=phone_number
        )
        return JsonResponse({'user' : 'exists'})
    except PhoneUser.DoesNotExist:
        return HttpResponseNotFound()
        
def generate_sms_code(request):
    "Функция генерации смс-кода и его записи в redis"
    #  Генерируем случайный шестизначный смс-код
    sms_code = randint(100000, 999999)    
    #  Снимаем js маску с номера, чтобы он состоял только из цифр
    phone_number = unmaskNumber(request.GET.get('phone_number'))
    #  Устанавливает значение смс-кода для номера в редис
    redis_connection.setex(phone_number, 900, sms_code)
    #  Выводит в консоль код, записанный в редис
    print('sms code -', sms_code, '  ', phone_number)
    return HttpResponse(status=200)
    
def sms_code_verification(request):
    "Функция подтверждения валидности введенего смс-кода и отправкой его статуса"
    data = request.GET
    #  Если login_status = True, то идёт авторизация, если False - регистрация
    login_status = True if data.get('login') == 'true' else False
    sms_code = data.get('sms_code')
    #  Снимаем js маску с номера, чтобы он состоял только из цифр
    phone_number = unmaskNumber(data.get('phone_number'))
    #  Получаем код из редиса
    stored_sms_code = redis_connection.get(phone_number).decode('utf-8')
    #  Если stored_sms_code = None, тогда срок его действия истёк
    if stored_sms_code is not None \
        and stored_sms_code == str(sms_code): 
            #  Если идёт авторизация - получаем модель пользователя
            if login_status:
                user = PhoneUser.objects.get(
                    phone_number=phone_number
                )
            #  Если идёт регистрация - создаём нового пользователя
            else:
                user = PhoneUser.objects.create_user(
                    phone_number=phone_number
                )
            #  Авторизуемся
            login(request, user)
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
