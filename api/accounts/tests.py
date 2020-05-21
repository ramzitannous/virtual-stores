from accounts.enums import AccountStatus
from accounts.models import Account
from shared.tests import BaseTestCase


class TestAccounts(BaseTestCase):

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

