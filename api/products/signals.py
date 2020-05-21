from django.dispatch import receiver
from django.db.models import signals

from .tasks import create_product_thumbnails, create_category_thumbnails
from products.models import ProductImage, Category


@receiver(signals.post_save, sender=ProductImage)
def receive_product_created(sender, instance: ProductImage, created, **kwargs):
    create_product_thumbnails.delay(str(instance.id))


@receiver(signals.post_save, sender=Category)
def receive_category_created(sender, instance: Category, created, **kwargs):
    create_category_thumbnails.delay(str(instance.id))
