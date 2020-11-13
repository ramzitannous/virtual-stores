from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.dispatch import receiver
from django.db.models import signals
from shared.fields import Base64ThumbnailField
from accounts.models import Account
from products.enum import ProductSize
from shared.models import BaseModel, BaseReview, OwnerModel
from versatileimagefield.fields import VersatileImageField, PPOIField
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
import math
from stores.models import Store


class Category(BaseModel):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, default=None, null=True)
    image = VersatileImageField("Image", ppoi_field="image_ppoi", upload_to=" category",
                                editable=True, null=True, blank=True)
    image_ppoi = PPOIField()

    class Meta:
        verbose_name_plural = "Categories"


class Product(OwnerModel):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.CharField(max_length=300, null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=False, blank=False)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="products", null=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products", null=True)

    price = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    discount_price = models.IntegerField(default=None, null=True)
    on_discount = models.BooleanField(default=False)

    colors = ArrayField(models.CharField(max_length=20), default=list)
    sizes = ArrayField(models.CharField(max_length=5), choices=[(s, s) for s in ProductSize], default=list)
    # shoe size and such
    integer_sizes = ArrayField(models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(45)]),
                               default=list)

    quantity = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    extras = JSONField(default=dict)

    def decrease_quantity(self, count=1):
        self.quantity -= count
        self.save()

    def create_discount(self, percentage):
        if percentage > 1:
            raise ValueError("discount can't be greater than 1")

        if percentage < 0:
            raise ValueError("discount can't be less than 0")
        discount = math.floor(percentage * self.price)
        self.discount_price = self.price - discount
        self.on_discount = True
        self.save()


class ProductReview(BaseReview):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")

    class Meta:
        verbose_name_plural = "Product Reviews"


class ProductImage(BaseModel):
    image = Base64ThumbnailField("Image", ppoi_field="image_ppoi", upload_to="product",
                                         editable=True, null=True, blank=True)
    image_ppoi = PPOIField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        verbose_name_plural = "Product Images"


@receiver(signals.post_save, sender=ProductImage)
def receive_product_created(sender, instance: ProductImage, created, **kwargs):
    from products.tasks import create_product_thumbnails
    create_product_thumbnails.delay(str(instance.id))


@receiver(signals.post_save, sender=Category)
def receive_category_created(sender, instance: Category, created, **kwargs):
    from products.tasks import create_category_thumbnails
    create_category_thumbnails.delay(str(instance.id))