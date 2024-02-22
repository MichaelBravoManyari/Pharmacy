from os import name
from django.db import models
from django.core.validators import MinValueValidator

"""To create a table in the pharmacy schema, 
    you must have created it before in the DB 
    and in this file in "class Meta: db_table" 
    change the "_" to \".\""""

class Presentation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'pharmacy_presentation'

    def __str__(self):
        return self.name


class Laboratory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=35, blank=True)
    representative = models.CharField(max_length=50, blank=True)
    observations = models.TextField(max_length=500, blank=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'pharmacy_laboratory'

    def __str__(self):
        return self.name


class Generic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'pharmacy_generic'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    lab = models.ForeignKey(Laboratory, on_delete=models.PROTECT)
    generic = models.ForeignKey(Generic, on_delete=models.PROTECT)
    presentation = models.ForeignKey(Presentation, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit_selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    min_stock = models.PositiveIntegerField()
    indications = models.TextField(max_length=500, blank=True)

    class Meta:
        db_table = 'pharmacy_product'

    def __str__(self):
        return self.name

