from    django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='login' ),
    path('inicio', views.inicio, name='inicio' ),
    path('historial', views.historial, name='historial' ),
    path('productos', views.productos, name='productos' ),
    path('productos/agregar', views.agregar, name='agregar' ),
    path('productos/editar', views.editar, name='editar' ),
    path('out', views.logout_request, name="out"),
]