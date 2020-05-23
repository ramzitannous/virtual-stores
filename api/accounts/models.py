from datetime import datetime

from versatileimagefield.fields import PPOIField
from django.contrib.auth.models import AbstractUser
from django.db import models
from shared.models import BaseModel, BaseAddress
from django.utils.translation import ugettext_lazy as _

from stores.models import Store
from shared.fields import Base64ThumbnailField
from .managers import AccountManager
from .enums import AccountTypes, AccountStatus, Gender


class AccountAddress(BaseAddress):
    pass


class Account(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    phone = models.CharField(max_length=100, blank=False, null=False, unique=True)
    image = Base64ThumbnailField("Image", ppoi_field="image_ppoi", upload_to="profile",
                                 editable=True, null=True, blank=True)
    image_ppoi = PPOIField()
    first_name = models.CharField(max_length=40, null=False, blank=False)
    last_name = models.CharField(max_length=40, null=False, blank=False)
    type = models.CharField(default=AccountTypes.NORMAL, max_length=10, choices=[(t, t) for t in AccountTypes])
    status = models.CharField(default=AccountStatus.UN_VERIFIED, max_length=20, choices=[(s, s) for s in AccountStatus])
    on_trial = models.BooleanField(default=True)
    deactivate_date = models.DateField(default=None, null=True)
    gender = models.CharField(max_length=1, choices=[(g, g) for g in Gender], null=False, blank=False)
    address = models.ForeignKey(AccountAddress, on_delete=models.CASCADE, default=None, null=True)

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
        self.deactivate_date = datetime.today()
        self.save()
        stores = Store.objects.filter(owner=self)
        for store in stores:
            store.deactivate()

    # todo check verified
    def reactivate(self):
        self.is_active = True
        self.on_trial = False
        self.deactivate_date = None
        self.status = AccountStatus.VERIFIED
        self.save()
        stores = Store.objects.filter(owner=self)
        for store in stores:
            store.reactivate()

    def delete(self, using=None, keep_parents=False):
        self.deactivate()
