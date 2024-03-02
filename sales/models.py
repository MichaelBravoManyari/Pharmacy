from django.db import models
from inventory.models import Product
from purchases.models import DocumentType
from django.core.validators import MinValueValidator
from datetime import date
from django.db.models import Max

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
    
    @classmethod
    def get_next_serie_and_numero(cls):
        max_serie = cls.objects.aggregate(Max('serie'))['serie__max']
        next_serie = 1 if max_serie is None else max_serie
        next_numero = cls.objects.filter(serie=next_serie).aggregate(Max('numero'))['numero__max']
        next_numero = 1 if next_numero is None else next_numero + 1
        if next_numero > 1000:
            next_serie += 1
            next_numero = 1
        return next_serie, next_numero


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