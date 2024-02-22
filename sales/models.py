from django.db import models
from inventory.models import Product
from purchases.models import DocumentType
from django.core.validators import MinValueValidator
from datetime import date

class Sale(models.Model):
    client = models.CharField(max_length=100, blank=True)
    serie = models.PositiveIntegerField()
    numero = models.PositiveIntegerField()
    date = models.DateField(default=date.today)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    details = models.ManyToManyField(Product, through='SaleDetail')

    class Meta:
        db_table = 'pharmacy_sale'
        constraints = [
            models.UniqueConstraint(fields=['serie', 'numero'], name="unique_sale")
        ]

    def __str__(self):
        return f"{self.serie}-{self.numero} {self.date}"


class SaleDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_sale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'pharmacy_sale_detail'
        constraints = [
            models.UniqueConstraint(fields=['sale', 'product'], name="unique_sale_detail")
        ]