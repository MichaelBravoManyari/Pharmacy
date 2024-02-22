from django.contrib import admin
from .models import Presentation, Generic, Laboratory, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']

admin.site.register(Presentation)
admin.site.register(Generic)
admin.site.register(Laboratory)
