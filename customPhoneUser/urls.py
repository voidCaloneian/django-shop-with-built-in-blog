from django.urls import path
from .views import *

urlpatterns = [
    path('login/', log_in, name='login'),
    path('logout/', log_out, name = 'logout'),
    path('check_phone_number/', check_phone_number, name='check_phone_number'),
    path('sms_code_verification/', sms_code_verification, name='sms_code_verification'),
    path('generate_sms_code/', generate_sms_code, name='generate_sms_code')
]