from django.contrib.auth.models import AbstractUser
from django.db import models
from shared.models import BaseModel
from django.utils.translation import ugettext_lazy as _

from stores.models import Store
from .managers import AccountManager
import uuid
from .enums import AccountTypes, AccountStatus


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return f"{instance.email}_{uuid.uuid4()}.{extension}"


class Account(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    phone = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to=upload_location, editable=True, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    type = models.CharField(default=AccountTypes.NORMAL, max_length=10, choices=[(t, t)for t in AccountTypes])
    status = models.CharField(default=AccountStatus.UN_VERIFIED, max_length=20, choices=[(s, s)for s in AccountStatus])
    on_trial = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.email

    def deactivate(self):
        self.is_active = False
        self.on_trial = False
        self.status = AccountStatus.UN_VERIFIED
        self.save()
        stores = Store.objects.filter(owner=self)
        for store in stores:
            store.deactivate()

    def delete(self, using=None, keep_parents=False):
        self.deactivate()
