from django.db import models

#provedores
class supliers (models.Model):
    suplier_id = models.AutoField(
          primary_key=True, 
          null=False)
    suplier_name = models.CharField(
         verbose_name='nombre',
           max_length=50,
             null=False)
    suplier_address = models.CharField(
         max_length=100)
    suplier_Tel = models.PositiveIntegerField(
         null=False)
    suplier_owner = models.CharField(
         max_length=50,
         null=False)

#categorias
class categories(models.Model):
        category_id =models.AutoField(primary_key=True, null=False)
        category_name =models.CharField(verbose_name='nombre', max_length=50)

#productos
class items(models.Model):
    item_id = models.AutoField(primary_key=True, null=False)
    item_name = models.CharField(verbose_name='producto', max_length=50, null=False)
    item_category_id = models.ForeignKey(categories, on_delete=models.CASCADE,null=False)
    item_suplier_id = models.ForeignKey(supliers, on_delete=models.CASCADE,null=False)

#posicion
class positions(models.Model):
    position_id = models.AutoField(primary_key=True, null=False)    
    posotion_index = models.PositiveIntegerField(null=False)
    position_aviable = models.CharField(max_length=50, null=False)

#stock
class stock(models.Model):
    stock_id = models.AutoField(primary_key=True, null=False)
    stock_item_id = models.ForeignKey(items, on_delete=models.CASCADE,null=False)
    stock_position_id = models.ForeignKey(positions, on_delete=models.CASCADE,null=False)

#usuarios
class users(models.Model):
    user_id = models.AutoField(verbose_name='nombre',primary_key=True, null=False)
    user_id =models.CharField(max_length=8, null=False)
    user_name =models.CharField(max_length=100, null=False)
    user_availability=models.BooleanField(null=False)

#stock tracking
class stock_tracking(models.Model):
    st_id = models.AutoField(primary_key=True, null=False)
    st_id_stock =models.ForeignKey(stock, on_delete=models.CASCADE,null=False)
    st_id_user =models.ForeignKey(users, on_delete=models.CASCADE,null=False)
    st_prev=models.IntegerField(null=True)
    st_act=models.IntegerField(null=True)


