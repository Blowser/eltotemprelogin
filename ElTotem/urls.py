# ElTotem/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# 🔥 Aquí va el conjuro visual, fuera de la lista
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#reset de tablitas