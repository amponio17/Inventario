from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
# Create your views here.

@login_required
def inicio(request):
   
    return render(request, 'paginas/PagP.html',
        
    )

@login_required
def login(request):
   
    return render(request, 'paginas/log.html',
        
    )

@login_required
def productos(request):
   
    return render(request, 'productos/vistaP.html',
        
    )

@login_required
def historial(request):
   
    return render(request, 'paginas/historial.html',
        
    )

@login_required
def agregar(request):
   
    return render(request, 'productos/agregar.html',
        
    )

@login_required
def editar(request):
   
    return render(request, 'productos/editar.html',
        
    )

def logout_request(request):
     logout(request)
     return render(request,'paginas/saliste.html')