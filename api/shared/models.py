from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
from django.conf import settings


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, help_text="UUID identify")
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class OwnerModel(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)

    class Meta:
        abstract = True


class BaseReview(OwnerModel):
    title = models.CharField(max_length=400, null=False, blank=False)
    rating = models.PositiveIntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        abstract = True


class BaseAddress(BaseModel):
    city = models.CharField(max_length=100, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    extra = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True
