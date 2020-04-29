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

initial1 = {
    "isbn" : "",
    "kitap_adi" : ""
}
initial2 = {
    "isbn" : "",
    "kitap_adi" : ""
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
def isbn_oku1(request):#admin
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
                    initial1["isbn"] = isbn
                    return redirect("kitap_ekle")
            
        return render(request, 'isbn_oku1.html', {'form' : form1,'alert' : alert})
    return Http404
def kitap_ekle(request):#admin
    if type(request) == type("") or request.user.is_superuser:
        form2 = KitapEkleForm2(request.POST or None,initial=initial1)
    
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
        form = KitapAraForm(request.POST or None)
        kitaplar = Kitap.objects.all()
        content = dict()
        
        if form.is_valid():
            kitap_listesi = list()
            sorgu = form.cleaned_data["arama"]

            for kitap in kitaplar:
                if sorgu in kitap.kitap_adi:
                    kitap_listesi.append(kitap)
                elif sorgu in kitap.isbn:
                    kitap_listesi.append(kitap)
            
            if len(kitap_listesi) == 0:
                content["kitaplar"] = None
            else:
                content["kitaplar"] = kitap_listesi
            
            form.clean()
            return render(request,"kitap_arama.html",{"form" : form,"content" : content})
        return render(request,"kitap_arama.html",{"form" : form,"content" : content})
    else:
        return Http404
def kitap_alma(request):#user
    if not request.user.is_superuser and request.user.is_authenticated:
        kitaplar = Kitap.objects.all()
        form = KitapAlForm(request.POST or None)
        
        if form.is_valid():
            alert = None
            isbn = form.cleaned_data["isbn"]
            
            if not Kitap.objects.filter(isbn=isbn).exists():#böyle bir kitap yoksa
                alert = {
                    "class" : "danger",
                    "message" : "isbn numarası hatalı!"
                }
                form.clean()

                return render(request,"kitap_alma.html",{"kitaplar" : kitaplar,"form" : form,"alert" : alert})
            else:#varsa
                kitap = Kitap.objects.get(isbn=isbn)
                kullanici = request.user
                print(kitap.kullanici) 
                if not kitap.kullanici:#raftaysa
                    kullanici_kitaplar = Kitap.objects.filter(kullanici = kullanici.id)
                    kullanici_kitap_sayisi = len(kullanici_kitaplar)
                    
                    if kullanici_kitap_sayisi >= 3:
                        alert = {
                        "class" : "danger",
                        "message" : "Sistemden en fazla üç kitap alabilirsiniz"
                        }
                        return render(request,"kitap_alma.html",{"kitaplar" : kitaplar,"form" : form,"alert" : alert})
                    elif kullanici_kitap_sayisi > 0:
                        for kitap1 in kullanici_kitaplar: 
                            sure = (Zaman.objects.get(id=1).tarih - kitap1.alinma_tarihi).days
                            
                            if sure >= 7:
                                alert = {
                                    "class" : "danger",
                                    "message" : "üzerinizde teslim tarihi geçmiş kitap var, yeni kitap alamazsınız"
                                }
                                return render(request,"kitap_alma.html",{"kitaplar" : kitaplar,"form" : form,"alert" : alert})
                        
                        kitap.kullanici = kullanici
                        kitap.alinma_tarihi = Zaman.objects.get(id=1).tarih
                        kitap.save()
                        alert = {
                                "class" : "success",
                                "message" : "Kitap bir haftalığına üzerinize tanımlandı"
                        }
                        return render(request,"kitap_alma.html",{"kitaplar" : kitaplar,"form" : form,"alert" : alert})
                    else:
                        kitap.kullanici = kullanici
                        kitap.alinma_tarihi = Zaman.objects.get(id=1).tarih
                        kitap.save()
                        alert = {
                                "class" : "success",
                                "message" : "Kitap bir haftalığına üzerinize tanımlandı"
                        }
                        return render(request,"kitap_alma.html",{"kitaplar" : kitaplar,"form" : form,"alert" : alert})

                    return render(request,"kitap_alma.html",{"kitaplar" : kitaplar,"form" : form,"alert" : alert})
                else:#kitap alınmışsa
                    alert = {
                        "class" : "danger",
                        "message" : "kitap zaten alınmış!"
                    }
                    
                    return render(request,"kitap_alma.html",{"kitaplar" : kitaplar,"form" : form,"alert" : alert})
                
            return render(request,"kitap_alma.html",{"kitaplar" : kitaplar,"form" : form,"alert" : alert})
        return render(request,"kitap_alma.html",{"kitaplar" : kitaplar,"form" : form})
    else:
        return Http404
def isbn_oku2(request):#user
    if type(request) != type("") and not request.user.is_superuser and request.user.is_authenticated:
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
                    initial2["isbn"] = isbn
                    return redirect("kitap_verme")
            
        return render(request, 'isbn_oku1.html', {'form' : form1,'alert' : alert})
    return Http404
def kitap_verme(request):#user
    if not request.user.is_superuser and request.user.is_authenticated:
        isbn = initial2["isbn"]
        alert = None
        form = None
        if not Kitap.objects.filter(isbn=isbn).exists():
            alert = "Kitap bulunamadı"
            return render(request, 'kitap_verme.html', {'form' : form,'alert' : alert})
        
        else:
            kitap = Kitap.objects.get(isbn=isbn)
            
            if not kitap.kullanici:
                alert = "Bu kitap zaten rafta"
                return render(request, 'kitap_verme.html', {'form' : form,'alert' : alert})
            elif kitap.kullanici.username != request.user.username:
                alert = "Bu kitap başkasının üzerinde"
                return render(request, 'kitap_verme.html', {'form' : form,'alert' : alert})

        initial2["kitap_adi"] = Kitap.objects.get(isbn=isbn).kitap_adi

        form = KitapVerForm(request.POST or None,initial=initial2)
        
        if form.is_valid():
            kitap = Kitap.objects.get(isbn=isbn)
            
            kitap.kullanici = None
            kitap.alinma_tarihi = None
            kitap.save()

            return redirect("isbn_oku2")
        return render(request, 'kitap_verme.html', {'form' : form,'alert' : alert})
    else:
        return Http404

def cikis(request):
    logout(request)
    return redirect("home")
# Create your views here.