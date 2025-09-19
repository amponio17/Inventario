from django.db import models

#provedores
class suppliers (models.Model):
    suplier_id = models.AutoField(
          primary_key=True,
          verbose_name='ID', 
          null=False)
    suplier_name = models.CharField(
         verbose_name='nombre',
           max_length=50,
             null=False)
    suplier_address = models.CharField(verbose_name='Email',
         max_length=100)
    suplier_tel = models.IntegerField(verbose_name='Celular',
         null=False)
    suplier_owner = models.CharField(verbose_name='Encargado',
         max_length=50,
         null=False)
    def __str__(self):
         return self.suplier_name

#categorias
class categories(models.Model):
        category_id =models.AutoField(
            primary_key=True,
            verbose_name='ID', 
            null=False),
        category_name =models.CharField(
            verbose_name='nombre',
              max_length=50)
        def __str__(self):
             return self.category_name


#productos
class items (models.Model):
    item_id = models.AutoField(primary_key=True, verbose_name='ID', null=False)
    item_name = models.CharField(verbose_name='producto', max_length=50, null=False)
    item_category_id = models.ForeignKey(categories, on_delete=models.CASCADE,null=False, verbose_name='Categoria')
    item_suplier_id = models.ForeignKey(suppliers, on_delete=models.CASCADE,null=False,verbose_name='Proveedor' ,)
    def __str__(self):
             return self.item_name
   
#posicion
class positions (models.Model):
    position_id = models.AutoField(primary_key=True, verbose_name='ID', null=False)    
    posotion_index = models.PositiveIntegerField(null=False)
    position_aviable = models.CharField(max_length=50, null=False)
    def __str__(self):
        return str(self.position_id )
#stock
class stock(models.Model):
    stock_id = models.AutoField(primary_key=True, verbose_name='ID', null=False,)
    stock_item_id = models.ForeignKey(items, on_delete=models.CASCADE,null=False,verbose_name='producto',)
    stock_position_id = models.ForeignKey(positions, on_delete=models.CASCADE,null=False,verbose_name='posicion',)
    
    stock_item_amount = models.IntegerField(verbose_name='Cantidad',default=0)
    stock_wanted = models.SmallIntegerField(null=False,verbose_name='Nesesarios',)
    def __str__(self):
        return str(self.stock_item_id)

#usuarios
class users (models.Model):
    user_id = models.AutoField( verbose_name='ID', primary_key=True, null=False)
    user_name =models.CharField(max_length=100, null=False,verbose_name='Nombre',)
    user_password =models.CharField(max_length=8, null=False,verbose_name='Contraseña',)
    user_availability=models.BooleanField(null=False,verbose_name='Activo',)
    def __str__(self):
             return self.user_name

#stock tracking
class stock_tracking(models.Model):
    st_id = models.AutoField(primary_key=True, verbose_name='ID',null=False)
    st_id_stock =models.ForeignKey(stock, on_delete=models.CASCADE,null=False,verbose_name='Stock del Producto',)
    st_id_user =models.ForeignKey(users, on_delete=models.CASCADE,null=False,verbose_name='Quien hace el movimiento',)
    st_prev=models.IntegerField(verbose_name='Stock anterior')
    st_act=models.IntegerField(verbose_name='Stock nuevo')
    def __str__(self):
        return str(self.st_id)
    


