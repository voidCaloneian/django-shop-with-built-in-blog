from django.http import HttpResponseRedirect
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.conf import settings


def indexRedirect(request):
    "Редирект с / на /shop/"
    #  reverse не использовал, так как работать тут не будет
    return HttpResponseRedirect('/shop/')

urlpatterns = [
    path('', indexRedirect),
    path('admin/', admin.site.urls),
    path('blog/', include('blogApp.urls')),
    path('shop/', include('shopApp.urls')),
    path('user/', include('customPhoneUser.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
