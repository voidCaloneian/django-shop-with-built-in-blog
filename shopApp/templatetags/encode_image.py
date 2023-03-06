from django.template.defaultfilters import register


@register.filter
def b64encode(value):
    image_b64 = base64.b64encode(value.encode('utf-8'))
    print(base64.b64encode(image_b64).decode('utf-8'))
    return base64.b64encode(image_b64).decode('utf-8')