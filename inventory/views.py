from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product

def search_products(request):
    product_name = request.GET.get('term')
    products = Product.objects.filter(name__icontains=product_name)
    
    product_list = [str(product.pk)+" - "+product.name for product in products]
    
    return JsonResponse(product_list, safe=False)

def get_product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    product_details = {
        'name': product.name,
        'lab' : product.lab.name,
        'generic': product.generic.name,
        'presentation': product.presentation.name,
        'quantity': product.quantity,
        'selling_price': product.selling_price,
        'unit_selling_price': product.unit_selling_price,
        'min_stock': product.min_stock,
        'indications': product.indications
    }

    return JsonResponse(product_details)


