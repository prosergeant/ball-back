from django.contrib import admin
from django.urls import path, include
from .settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
  + static(STATIC_URL, document_root=STATIC_ROOT)
