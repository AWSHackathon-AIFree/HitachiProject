from .views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

