from django.shortcuts import render,HttpResponse

def home(request):
    if request.user.is_superuser:
        return HttpResponse("<b>Superuser</b>")
    elif request.user.is_authenticated:
        return HttpResponse("<h1>user</h1>")
    else:
        return render(request,"login.html")

    
        
    
    
# Create your views here.