from django.shortcuts import render,HttpResponse,Http404,redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

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

def kitap_ekle(request):#admin
    if request.user.is_superuser:
        return render(request,"kitap_ekle.html")
    else:
        return Http404
def zaman_atla(request):#admin
    if request.user.is_superuser:
        return render(request,"zaman_atla.html")
    else:
        return Http404
def kullanici_listele(request):#admin
    if request.user.is_superuser:
        return render(request,"kullanici_listele.html")
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
# Create your views here.