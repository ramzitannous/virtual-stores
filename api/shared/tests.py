from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.enums import AccountTypes, AccountStatus
from accounts.models import Account


class BaseTestCase(APITestCase):
    VERSION = "v1"

    def setUp(self) -> None:
        self.account = Account.objects.create(email="Test User",
                                              first_name="Test", last_name="USer",
                                              phone="1234", type=AccountTypes.BUSINESS, status=AccountStatus.VERIFIED)

        self.account.set_password("Test User")
        self.account.save()
        self.client.force_login(self.account)
        self.normal_account = Account.objects.create(email="Test User1",
                                                     password="Test User", first_name="Test", last_name="USer",
                                                     phone="1234", type=AccountTypes.NORMAL)

    def resolve_url(self, url, **kwargs):
        return reverse(url, kwargs={"version": self.VERSION, **kwargs})

    def tearDown(self) -> None:
        self.account.delete()
