from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Artık index diye bir view'a ihtiyacımız yok, silebilirsin:
    # path('', views.index, name='index'), 
    
    path('kitaplar/', views.kitap_listesi, name='kitap_listesi'), 
    path('kitaplar/<int:pk>/', views.kitap_detay, name='kitap_detay'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]