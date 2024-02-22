from django.db import models, transaction
from inventory.models import Product
from django.core.validators import MinValueValidator

class DocumentType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'pharmacy_document_type'

    def __str__(self):
        return self.name


class Provider(models.Model):
    ruc = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'pharmacy_provider'

    def __str__(self):
        return self.name


class Purchase(models.Model):
    date = models.DateField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    series = models.CharField(max_length=500)
    number = models.CharField(max_length=100)
    details = models.ManyToManyField(Product, through='PurchaseDetail')
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    igv = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'pharmacy_purchase'
        constraints = [
            models.UniqueConstraint(fields=['series', 'number', 'provider'], name='unique_purchase')
        ]

    def __str__(self):
        return f"{self.provider} {self.date}"

class PurchaseDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    lot = models.CharField(max_length=100)
    expiration_date = models.DateField()
    quantity = models.PositiveIntegerField()
    unit_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'pharmacy_purchase_detail'
        constraints = [
            models.UniqueConstraint(fields=['purchase', 'product'], name="unique_purchase_detail")
        ]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_quantity = PurchaseDetail.objects.get(pk=self.pk).quantity
                self.product.quantity -= old_quantity

            self.product.quantity += self.quantity
            self.product.save()

            super().save(*args, **kwargs)
