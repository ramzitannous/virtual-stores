from datetime import datetime

from versatileimagefield.fields import PPOIField

from shared.fields import Base64ThumbnailField
from django.db import models
from shared.models import OwnerModel, BaseModel, BaseReview
from django.contrib import admin


class StoreAddress(BaseModel):
    city = models.CharField(max_length=100, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    extra = models.CharField(max_length=200, null=True, blank=True)


class Store(OwnerModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    image = Base64ThumbnailField(null=True, editable=True, blank=False)
    image_ppoi = PPOIField()
    phone = models.CharField(null=False, blank=False, max_length=20)
    address = models.ForeignKey(StoreAddress, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    deactivate_date = models.DateField(default=None, null=True)

    def delete(self, using=None, keep_parents=False):
        self.deactivate()

    def deactivate(self):
        self.is_active = False
        self.deactivate_date = datetime.today()
        self.save()
        for product in self.products.filter(is_active=True):
            product.is_active = False
            product.save()

    def reactivate(self):
        self.is_active = True
        self.deactivate_date = None
        self.save()
        for product in self.products.filter(is_active=False):
            product.is_active = True
            product.save()


class StoreReview(BaseReview):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="reviews")


@admin.register(StoreAddress)
class StoreAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(StoreReview)
class StoreReviewAdmin(admin.ModelAdmin):
    pass
