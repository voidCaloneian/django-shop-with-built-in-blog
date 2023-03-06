from django.template import Library


register = Library()

@register.simple_tag
def beautify(phone_number: str) -> str:
    "Возвращает номер телефона в виде +7 (999) 999 99 99"
    _ = phone_number  #  Для более читабельного форматирования
    beautified_phone_number = '+{} ({}) {} {}'.format(
        _[0], _[1:4], _[4:7], _[7:]
    )
    
    return beautified_phone_number
    