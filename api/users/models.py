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
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.email
