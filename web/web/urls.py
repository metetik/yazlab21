"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"),
    path('kitap_ekle/',kitap_ekle,name="kitap_ekle"),
    path('kullanici_listele/',kullanici_listele,name="kullanici_listele"),
    path('zaman_atla/',zaman_atla,name="zaman_atla"),
    path('kitap_arama/',kitap_arama,name="kitap_arama"),
    path('kitap_alma/',kitap_alma,name="kitap_alma"),
    path('kitap_verme/',kitap_verme,name="kitap_verme"),
    path('cikis/',cikis,name="cikis"),
]
