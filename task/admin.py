from django.contrib import admin
from .models import Provedor
from .models import categoria
from .models import productos
from .models import posicione
from .models import usuarios
from .models import stock
from .models import stock_tracking
# Register your models here.




#vista de datos de provedor 
@admin.register(Provedor)
class Provedor(admin.ModelAdmin):
    list_display=('suplier_id', 'suplier_name','suplier_Tel','suplier_address','suplier_owner')


#vista de datos de productos
@admin.register(productos)
class productos(admin.ModelAdmin):
    list_display=('item_id', 'item_name', 'item_category_id','item_suplier_id')

#vista de datos de usuarios
@admin.register(usuarios)
class usuarios(admin.ModelAdmin):
    list_display=('user_id', 'user_name', 'user_availability')

#vista de datos de stock
@admin.register(stock)
class stock(admin.ModelAdmin):
    list_display=('stock_id', 'stock_item_id', 'stock_position_id', 'stock_itme_amount', 'stock_deseado')

#vista de datos de stock_tracking
@admin.register(stock_tracking)
class stock_tracking(admin.ModelAdmin):
    list_display=('st_id', 'st_id_stock', 'st_id_user', 'st_prev', 'st_act')

#vista de datos de categoria
@admin.register(categoria)
class categoria(admin.ModelAdmin):
    list_display=('category_name',)

#vista de datos de categoria
@admin.register(posicione)
class posicione(admin.ModelAdmin):
    list_display=('position_id','posotion_index','position_aviable',)

#admin.site.register(categoria),
#admin.site.register(posicione),
#admin.site.register(usuarios),
#admin.site.register(stock),
#dmin.site.register(stock_tracking),
