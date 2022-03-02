from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from core.views import *
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', searchView, name='searchform'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
