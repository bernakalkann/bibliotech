from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Tüm kitap_app isteklerini 'api/' çatısı altına topladık
    path('api/', include('kitap_app.urls')), 
]