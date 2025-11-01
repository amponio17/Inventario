from django import forms
from .models import items, suppliers, categories, positions, stock

class ItemForm(forms.ModelForm):
    class Meta:
        model = items
        fields = ['item_name', 'item_category_id', 'item_suplier_id']
        labels = {
            'item_name': 'Nombre del Producto',
            'item_category_id': 'Categoría',
            'item_suplier_id': 'Proveedor',
        }

    def clean_item_name(self):
        name = self.cleaned_data.get('item_name')
        if items.objects.filter(item_name=name).exists():
            raise forms.ValidationError("El nombre del producto ya existe.")
        return name
    
class StockForm(forms.ModelForm):
    class Meta:
        model = stock
        fields = ['stock_item_id', 'stock_position_id', 'stock_item_amount', 'stock_wanted']
