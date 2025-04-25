from    django.urls import path
from . import views

urlpatterns = [
    path('', views.log, name='log' ),
    path('inicio', views.inicio, name='inicio' ),
    path('historial', views.historial, name='historial' ),
    path('productos', views.productos, name='productos' ),
    path('productos/agregar', views.agregar, name='agregar' ),
    path('productos/editar', views.editar, name='editar' ),
]