from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from shared.models import OwnerModel, BaseModel
from django.contrib import admin


class StoreAddress(BaseModel):
    city = models.CharField(max_length=100, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    extra = models.CharField(max_length=200, null=True, blank=True)


class Store(OwnerModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    image = models.ImageField(null=True, editable=True, blank=False)
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


class StoreReview(OwnerModel):
    title = models.CharField(max_length=400, null=False, blank=False)
    rating = models.PositiveIntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(5)])
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


@admin.register(StoreAddress)
class StoreAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(StoreReview)
class StoreReviewAdmin(admin.ModelAdmin):
    pass
