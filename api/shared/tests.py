from django.urls import reverse
from rest_framework.test import APITestCase
from shared.factories import BusinessAccountFactory, NormalAccountFactory


class BaseTestCase(APITestCase):
    VERSION = "v1"

    def setUp(self) -> None:
        self.account = BusinessAccountFactory()
        self.account.set_password("Test User")
        self.account.save()
        self.client.force_login(self.account)
        self.normal_account = NormalAccountFactory()
        self.normal_account.set_password("test")
        self.normal_account.save()

    def resolve_url(self, url, **kwargs):
        return reverse(url, kwargs={"version": self.VERSION, **kwargs})

    def tearDown(self) -> None:
        self.account.delete()
        self.normal_account.delete()
