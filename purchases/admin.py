from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError
from .models import DocumentType, Provider, Purchase, PurchaseDetail

class PurchaseDetailInLineFormSet(BaseInlineFormSet):
    def is_valid(self):
        return super(PurchaseDetailInLineFormSet, self).is_valid() and \
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
            raise ValidationError('Debe haber al menos un detalle de compra')

class PurchaseDetailInLine(admin.TabularInline):
    model = PurchaseDetail
    formset = PurchaseDetailInLineFormSet

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseDetailInLine]

admin.site.register(DocumentType)
admin.site.register(Provider)