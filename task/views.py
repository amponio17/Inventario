from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from .forms import ItemForm
# Create your views here.

@login_required
def inicio(request):
   
    return render(request, 'paginas/PagP.html',
        
    )

# @login_required
# def login(request):
   
#     return render(request, 'paginas/log.html',
        
#     )

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
        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Producto agregado exitosamente.")
                return redirect('agregar')  # Redirige a la vista de productos después de guardar
            else:
                messages.error(request, "Error al agregar el producto. Por favor, verifica los datos ingresados.")
        else:
            form = ItemForm()  # Vuelve a mostrar el formulario vacío si no es válido
        return render(request, 'productos/agregar.html', {'form': form})

@login_required
def editar(request):
   
    return render(request, 'productos/editar.html',
        
    )

def logout_request(request):
     logout(request)
     return render(request,'paginas/saliste.html')