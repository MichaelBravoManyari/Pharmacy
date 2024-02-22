from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import SaleForm, SaleDetailForm
from django.db import transaction
from .models import Sale, SaleDetail
from inventory.models import Product

def create_sale(request):
    SaleDetailFormSet = inlineformset_factory(Sale, SaleDetail, form=SaleDetailForm, extra=1, can_delete=True)

    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        sale_detail_formset = SaleDetailFormSet(request.POST, prefix='sale_detail')

        if sale_form.is_valid() and sale_detail_formset.is_valid():
            with transaction.atomic():
                sale = sale_form.save()

                for form in sale_detail_formset:
                    sale_detail = form.save(commit=False)
                    sale_detail.sale = sale
                    sale_detail.total = sale_detail.quantity * sale_detail.unit_sale_price

                    # Si se proporciona un nombre de producto, busca el producto y asigna la instancia al detalle de venta
                    product_name = form.cleaned_data.get('product_name')
                    if product_name:
                        product = Product.objects.filter(name__iexact=product_name).first()
                        if product:
                            sale_detail.product = product

                    sale_detail.save()

                    # Actualizar el stock del producto
                    if sale_detail.product:
                        sale_detail.product.quantity -= sale_detail.quantity
                        sale_detail.product.save()

            return redirect('ventas')  # Ajusta la redirección según tus necesidades
    else:
        sale_form = SaleForm()
        sale_detail_formset = SaleDetailFormSet(prefix='sale_detail')

    return render(request, 'sales/create_sale.html', {'sale_form': sale_form, 'sale_detail_formset': sale_detail_formset})
