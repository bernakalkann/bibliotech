from django.contrib import admin

# kayit aracidir, ayni zamanda veri yonetim merkezidir!!!!
from django.contrib import admin
from .models import Kitap

admin.site.register(Kitap)  #modeli kaydediyoruz
