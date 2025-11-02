from    django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='login' ),
    path('inicio', views.inicio, name='inicio' ),
    path('historial', views.historial, name='historial' ),
    path('productos', views.productos, name='productos' ),
    path('productos/agregar', views.agregar, name='agregar' ),
    path('productos/editar/<int:pk>/', views.editar_stock, name='editar_stock'),
    path('productos/eliminar/<int:pk>/', views.eliminar_stock, name='eliminar_stock'),
    path('out', views.logout_request, name="out"),
]