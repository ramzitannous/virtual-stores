from celery import shared_task

from products.models import ProductImage
from shared.utils import create_thumbnails


@shared_task
def create_product_thumbnails(product_image_id: str):
    create_thumbnails(product_image_id, ProductImage, "product")
