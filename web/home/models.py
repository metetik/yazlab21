from django.db import models

class Kitap(models.Model):
    isbn = models.CharField(max_length=13)
    kitap_adi = models.CharField(max_length=50)
    #kullanıcı silinirse default value olarak ayarla
    kullanici = models.ForeignKey("auth.User",related_name="kitaplar",default=None,\
        null=True,on_delete=models.SET_NULL)
    alinma_tarihi = models.DateField(auto_now=False, auto_now_add=False,null=True)