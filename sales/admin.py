from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError
from sales.forms import SaleForm
from .models import Sale, SaleDetail

class SaleDetailInLineFormSet(BaseInlineFormSet):
    def is_valid(self):
        return super(SaleDetailInLineFormSet, self).is_valid() and \
                    not any([bool(e) for e in self.errors])
    
    def clean(self):          
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    count += 1
            except AttributeError:
                pass
        if count < 1:
            raise ValidationError('Debe haber al menos un detalle de venta')

class SaleDetailInLine(admin.TabularInline):
    model = SaleDetail
    formset = SaleDetailInLineFormSet

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    change_form_template = "sales/create_sale.html"
    inlines = [SaleDetailInLine]
