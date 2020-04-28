from django import forms
from django.contrib.auth import authenticate
from .models import *
import os
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Kullanıcı Adı")
    password = forms.CharField(max_length=100, label="Parola", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Kullanıcı adı veya parola hatalı..")
            
            return super(LoginForm,self).clean()


class KitapEkleForm1(forms.Form):
    resim = forms.FileField(required=False)    
    
class KitapEkleForm2(forms.Form):
    isbn = forms.CharField(max_length=13,disabled=True,required=False)
    kitap_adi = forms.CharField(max_length=50,required=False)

    