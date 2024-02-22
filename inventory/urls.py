from django.urls import path
from .views import search_products, get_product_details

app_name = "inventory"
urlpatterns = [
    path('search_products/', search_products, name='search_products'),
    path('get_product_details/<int:product_id>/', get_product_details, name='get_product_details'),
]
