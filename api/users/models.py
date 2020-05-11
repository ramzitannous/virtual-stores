from django.contrib.auth.models import AbstractUser
from django.db import models
from shared.models import BaseModel
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
import uuid


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return f"{instance.email}_{uuid.uuid4()}.{extension}"


class CustomUser(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    phone = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to=upload_location, editable=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
