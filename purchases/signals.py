from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import PurchaseDetail
from django.db import transaction

@receiver(pre_delete, sender=PurchaseDetail)
def delete_purchase_detail(sender, instance, **kwargs):
    with transaction.atomic():
        instance.product.quantity -= instance.quantity
        instance.product.save()