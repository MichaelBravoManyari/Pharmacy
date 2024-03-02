from django.urls import path
from .views import create_sale

app_name="sales"
urlpatterns = [
    path('create_sale/', create_sale, name='create_sale'),
]
