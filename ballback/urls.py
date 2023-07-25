from django.contrib import admin
from django.urls import path, include
from .settings import MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
