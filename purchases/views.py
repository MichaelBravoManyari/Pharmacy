from django.shortcuts import render
from .models import DocumentType
from django.http import JsonResponse

def get_document_types(request):
    document_types = DocumentType.objects.all().values('pk', 'name')
    return JsonResponse(list(document_types), safe=False)
