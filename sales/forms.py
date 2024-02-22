from django import forms
from .models import Sale, SaleDetail

class SaleForm(forms.ModelForm):
    product = forms.CharField(max_length=100, label='Producto', required=True, widget=forms.TextInput(attrs={'cls': 'id_product_name'}))

    class Meta:
        model = Sale
        fields = ['product','client', 'date', 'document_type']

    class Media:
        js = ('sales/js/script.js',)

class SaleDetailForm(forms.ModelForm):
    class Meta:
        model = SaleDetail
        fields = ['product', 'quantity', 'unit_sale_price', 'total']
