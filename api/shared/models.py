from django.db import models
import uuid
from django.conf import settings


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, help_text="UUID identify")
    create_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnerModel(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True
