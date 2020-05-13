from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import CustomUser


class BaseTestCase(APITestCase):
    VERSION = "v1"

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="Test User",
                                              password="Test User", first_name="Test", last_name="USer", phone="1234")
        self.client.force_login(self.user)

    def resolve_url(self, url, **kwargs):
        return reverse(url, kwargs={"version": self.VERSION, **kwargs})

    def tearDown(self) -> None:
        self.user.delete()
