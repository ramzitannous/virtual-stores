from django.dispatch import receiver
from django.db.models import signals

from .tasks import create_product_thumbnails
from products.models import Product, ProductImage


@receiver(signals.post_save, sender=ProductImage)
def create_thumbnails(sender, instance: Product, created, **kwargs):
    create_product_thumbnails.delay(str(instance.id))
