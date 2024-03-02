import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Sale, DocumentType, SaleDetail, Product
from django.core.exceptions import ValidationError

def create_sale(request):
    datos_venta = json.loads(request.POST.get('sale_data'))
    datos_detalles_venta = json.loads(request.POST.get('sale_details')) 

    serie_siguiente, numero_siguiente = Sale.get_next_serie_and_numero()

    tipo_documento_valor = datos_venta['document_type']
    tipo_documento = get_object_or_404(DocumentType, pk=tipo_documento_valor)

    try:
        venta = Sale.objects.create(
            client=datos_venta['client'],
            serie=serie_siguiente,
            numero=numero_siguiente,
            document_type=tipo_documento,
        )

        detalles_venta = []
        for detalle in datos_detalles_venta:
            producto = get_object_or_404(Product, pk=detalle['productId']) 

            if producto.quantity < int(detalle['quantity']):
                    raise ValidationError(f"No hay suficiente stock para {producto.name}")

            detalle_venta = SaleDetail(
                sale=venta,
                product=producto,
                quantity=detalle['quantity'],
                unit_sale_price=detalle['price'],  # Use el nombre de campo correcto
                total=detalle['total'],
            )

            detalles_venta.append(detalle_venta)

            producto.quantity -= int(detalle['quantity'])
            producto.save()

        SaleDetail.objects.bulk_create(detalles_venta)

        return JsonResponse({'message': 'Venta registrada exitosamente'})
    except ValidationError as e:
        mensaje_error = str(e)
        return JsonResponse({'error': mensaje_error}, status=400)