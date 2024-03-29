from accounts.enums import AccountStatus
from accounts.models import Account
from shared.tests import BaseTestCase


class TestAccounts(BaseTestCase):
    payload = {
        "email": "test@gmail.com",
        "password": "test@123",
        "re_password": "test@123",
        "image": "data:image/png;base64,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",
        "phone": "0597221253",
        "first_name": "test",
        "last_name": "admin",
        "gender": "M",
        "type": "BUSINESS",
        "address": {
            "city": "test city",
            "street": "test street"
        }
    }

    def assert_account_deactivated(self):
        account = Account.objects.get(id=self.account.id)
        assert account.is_active is False
        assert account.status == AccountStatus.UN_VERIFIED
        assert account.on_trial is False
        assert account.deactivate_date is not None

    def test_deactivate_account(self):
        self.account.deactivate()
        self.assert_account_deactivated()

    def test_delete_account_api(self):
        url = self.resolve_url("accounts-me")
        res = self.client.delete(url, {"current_password": "Test User"})
        assert res.status_code == 204
        self.assert_account_deactivated()

    def test_edit_account(self):
        url = self.resolve_url("accounts-me")
        res = self.client.patch(url, {"image": self.get_image()})
        assert res.status_code == 200
        account = self.client.get(url)
        assert len(account.json()["image"]) == 2
        self.account.refresh_from_db()
        self.account.image.delete()

    def test_create_account(self):
        url = self.resolve_url("accounts-list")
        res = self.client.post(url, self.payload)
        assert res.status_code == 201
        assert res.json()["address"]["city"] == self.payload["address"]["city"]
        account = Account.objects.select_related("address").get(id=res.json()["id"])
        assert account.address is not None

    def test_edit_address(self):
        url = self.resolve_url("accounts-me")
        city = "Test City"
        test_name = "test"
        res = self.client.patch(url, {"address": {"city": city}, "lastName": test_name})
        assert res.status_code == 200
        account = Account.objects.select_related("address").get(id=res.json()["id"])
        assert account.address.city == city
        assert account.last_name == test_name

