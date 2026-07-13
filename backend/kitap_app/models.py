from django.db import models

# Create your models here.
from django.db import models

class Kitap(models.Model):
    baslik = models.CharField(max_length=200)
    yazar = models.CharField(max_length=100)
    fav = models.BooleanField(default=False)
    sku = models.CharField(max_length=50, null=True, blank=True)
    fiyat = models.FloatField()
    adet = models.IntegerField()
    tedarikci = models.CharField(max_length=100)
    def __str__(self):
        return self.baslik