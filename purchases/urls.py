from django.urls import path
from .views import get_document_types

app_name="purchases"
urlpatterns = [
    path('get_document_types/', get_document_types, name='get_document_types'),
]