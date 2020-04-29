from django.shortcuts import render,HttpResponse,Http404,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
import logging
from .functions import resim_oku
from django.utils import timezone
import datetime
import locale
from django.contrib.auth.models import User

locale.setlocale(locale.LC_ALL, '')

initial = {
    "isbn" : "1",
    "kitap_adi" : "2"
}
def home(request):
    if request.user.is_superuser:
        return render(request,"admin_home.html")
    elif request.user.is_authenticated:
        return render(request,"user_home.html")
    else:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')

        return render(request, 'login.html', {'form' : form})

def isbn_oku(request):#admin
    if type(request) != type("") and request.user.is_superuser:
        form1 = KitapEkleForm1(request.POST or None,request.FILES or None)
        alert = None
        if form1.is_valid():
            resim_adi = form1.cleaned_data["resim"]
            if resim_adi:
                isbn = resim_oku(resim_adi.name)
                print(isbn)
                if isbn == "None":
                    alert = "Resim okunamadı"
                else:
                    initial["isbn"] = isbn
                    return redirect("kitap_ekle")
            
        return render(request, 'isbn_oku.html', {'form' : form1,'alert' : alert})
    return Http404
def kitap_ekle(request):#admin
    if type(request) == type("") or request.user.is_superuser:
        form2 = KitapEkleForm2(request.POST or None,initial=initial)
    
        if form2.is_valid():
            print("b")
            ktp = Kitap()
            ktp.isbn = form2.cleaned_data["isbn"]
            ktp.kitap_adi = form2.cleaned_data["kitap_adi"]
            ktp.kullanici = None
            ktp.alinma_tarihi = None
            ktp.save()

            return redirect("isbn_oku")
        return render(request, 'kitap_ekle.html', {'form' : form2})
    return Http404    
def zaman_atla(request):#admin
    if request.user.is_superuser:
        tarih = Zaman.objects.get(id=1)
        yil = datetime.datetime.strftime(tarih.tarih, '%Y') 
        ay = datetime.datetime.strftime(tarih.tarih, '%B')
        gun = datetime.datetime.strftime(tarih.tarih, '%d')
        zaman = gun + " " + ay + " " + yil
        form = ZamanAtlaForm(request.POST or None)

        if form.is_valid():
            atlanacak_gun = int(form.cleaned_data["gun"])
            atlanacak = datetime.timedelta(days=atlanacak_gun)
            tarih.tarih += atlanacak
            tarih.save()
            return redirect("zaman_atla")

        return render(request,"zaman_atla.html",{"zaman" : zaman,"form" : form})
    else:
        return Http404
def kullanici_listele(request):#admin
    if request.user.is_superuser:
        tum_kullanicilar = User.objects.filter(is_superuser=False)
        kitaplar = Kitap.objects.all()
        context = {"kullanicilar" : tum_kullanicilar,
                   "kitaplar" : kitaplar
                   }

        return render(request,"kullanici_listele.html",context)
    else:
        return Http404
def kitap_arama(request):#user
    if not request.user.is_superuser and request.user.is_authenticated:
        return render(request,"kitap_arama.html")
    else:
        return Http404
def kitap_alma(request):#user
    if not request.user.is_superuser and request.user.is_authenticated:
        return render(request,"kitap_alma.html")
    else:
        return Http404
def kitap_verme(request):#user
    if not request.user.is_superuser and request.user.is_authenticated:
        return render(request,"kitap_verme.html")
    else:
        return Http404
def cikis(request):
    logout(request)
    return redirect("home")
# Create your views here.