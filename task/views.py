from django.shortcuts import render

# Create your views here.

def inicio(request):
   
    return render(request, 'paginas/PagP.html',
        
    )
def log(request):
   
    return render(request, 'paginas/log.html',
        
    )
def productos(request):
   
    return render(request, 'productos/vistaP.html',
        
    )
def historial(request):
   
    return render(request, 'paginas/historial.html',
        
    )
def agregar(request):
   
    return render(request, 'productos/agregar.html',
        
    )
def editar(request):
   
    return render(request, 'productos/editar.html',
        
    )
