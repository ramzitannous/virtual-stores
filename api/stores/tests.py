from shared.factories import CategoryFactory
from shared.tests import BaseTestCase
from stores.models import Store
from accounts.models import Account


class TestStoreCreate(BaseTestCase):
    payload = {
        "name": "Test Store",
        "description": "test description",
        "phone": "asdfasdf",
        "openTime": "12:00:PM",
        "closeTime": "12:00:PM",
        "address": {
            "city": "ramallah",
            "street": "batten al hawa",
            "extra": "near"
        }
    }

    def setUp(self) -> None:
        super().setUp()
        cat = CategoryFactory()
        self.payload["category_id"] = str(cat.id)
        self.url = self.resolve_url("stores-list")

    def test_create_store_authenticated(self):
        self.payload["image"] = self.get_image()
        response = self.client.post(self.url, self.payload)
        assert response.data is not None
        assert response.status_code == 201
        store = Store.objects.get(id=response.data["id"])
        store.image.delete()
        store.delete()
        del self.payload["image"]

    def test_create_store_not_authenticated(self):
        self.client.logout()

        response = self.client.post(self.url, self.payload)
        assert response.status_code == 401

    def test_list_unauthenticated(self):
        self.client.force_login(self.account)
        response = self.client.post(self.url, self.payload)
        self.client.logout()
        list_response = self.client.get(self.url)
        assert list_response.status_code == 200
        assert len(list_response.data["results"]) == 1
        Store.objects.get(id=response.data["id"]).delete()

    def test_unauthenticated_list_only_active(self):
        self.client.force_login(self.account)
        self.client.post(self.url, self.payload)
        self.payload["name"] = "tt"
        res = self.client.post(self.url, self.payload)
        store = Store.objects.get(id=res.json()["id"])
        store.is_active = False
        store.save()
        self.client.logout()
        list_response = self.client.get(self.url)
        assert list_response.status_code == 200
        assert len(list_response.data["results"]) == 1

    def test_allow_update_store(self):
        self.client.force_login(self.account)
        response = self.client.post(self.url, self.payload)
        _id = response.data["id"]
        res = self.client.patch(self.resolve_url("stores-detail", pk=_id), {"name": "test"})
        assert res.status_code == 200

    def test_deny_update_store(self):
        response = self.client.post(self.url, self.payload)
        self.client.logout()
        account = Account.objects.create(email="ramzi", password="451")
        self.client.force_login(account)
        res = self.client.patch(self.resolve_url("stores-detail", pk=response.data["id"]), {"name": "test"})
        assert res.status_code == 403

    def test_change_active(self):
        response = self.client.post(self.url, self.payload)
        res = self.client.patch(self.resolve_url("stores-detail", pk=response.data["id"]), {"isActive": False})
        assert res.status_code == 200
        assert res.json()["isActive"]

    def test_description(self):
        response = self.client.post(self.url, self.payload)
        desc = "new Description"
        res = self.client.patch(self.resolve_url("stores-detail", pk=response.data["id"]),
                                {"description": desc})
        assert res.status_code == 200
        store = Store.objects.get(id=response.json()["id"])
        assert store.description == desc

    def test_duplicate_name(self):
        self.client.post(self.url, self.payload)
        res = self.client.post(self.url, self.payload)
        assert res.status_code == 400

    def test_edit_address(self):
        response = self.client.post(self.url, self.payload)
        extra = "test extra"
        res = self.client.patch(self.resolve_url("stores-detail", pk=response.data["id"]),
                                {"address": {"extra": extra}})
        assert res.status_code == 200
        store = Store.objects.get(id=response.json()["id"])
        assert store.address.extra == extra

    def test_edit_store(self):
        response = self.client.post(self.url, self.payload)
        extra = "test extra"
        name = "hello"
        res = self.client.patch(self.resolve_url("stores-detail", pk=response.data["id"]),
                                {"address": {"extra": extra}, "name": name})
        assert res.status_code == 200
        data = res.json()
        assert data["address"]["extra"] == extra
        assert data["name"] == name
        store = Store.objects.get(id=data["id"])
        assert store.address.extra == extra
        assert store.name == name

    def test_prevent_delete_by_other_account(self):
        res = self.client.post(self.url, self.payload)
        self.client.logout()
        account = Account.objects.create(email="ramzi", password="451")
        self.client.force_login(account)
        response = self.client.delete(self.resolve_url("stores-detail", pk=res.data["id"]))
        assert response.status_code == 403

    def test_add_a_review(self):
        res = self.client.post(self.url, self.payload)
        store_id = res.json()["id"]
        url = self.resolve_url("stores-review-list", store_id=store_id)
        res = self.client.post(url, {
            "title": "hello",
            "rating": 5
        })

        assert res.status_code == 201

        res = self.client.post(self.resolve_url("stores-review-list", store_id=store_id), {
            "title": "hello",
            "rating": 5
        })

        assert res.status_code == 201

        reviews_res = self.client.get(url)
        reviews = reviews_res.json()["results"]
        assert len(reviews) == 2
        assert reviews[0]["owner"]["id"] == str(self.account.id)
        assert reviews[0]["owner"]["fullName"] == str(self.account.get_full_name())

    def test_prevent_delete_review_by_other_account(self):
        res = self.client.post(self.url, self.payload)
        store_id = res.json()["id"]
        url = self.resolve_url("stores-review-list", store_id=res.json()["id"])
        res = self.client.post(self.resolve_url("stores-review-list", store_id=store_id), {
            "title": "hello",
            "rating": 5
        })
        self.client.logout()
        account = Account.objects.create(email="ramzi", password="451")
        self.client.force_login(account)
        response = self.client.delete(self.resolve_url("stores-review-detail", pk=res.data["id"]))
        assert response.status_code == 403

    def test_normal_account_create(self):
        self.client.force_login(self.normal_account)
        res = self.client.post(self.url, self.payload)
        assert res.status_code == 403

    def test_check_reviews_count_avg(self):
        res = self.client.post(self.url, self.payload)
        store_id = res.json()["id"]
        url = self.resolve_url("stores-review-list", store_id=store_id)
        self.client.post(url, {
            "title": "hello",
            "rating": 4
        })

        self.client.post(self.resolve_url("stores-review-list", store_id=store_id), {
            "title": "hello",
            "rating": 5
        })

        res = self.client.get(self.url)
        store = res.json()["results"][0]
        assert store["reviewsAvg"] == 4.5
        assert store["reviewsCount"] == 2

    def test_account_can_list_his_stores(self):
        res = self.client.post(self.url, self.payload)
        store_id = res.json()["id"]
        res = self.client.get(self.resolve_url("stores-me"))
        stores = res.json()["results"]
        assert len(stores) == 1
        assert stores[0]["id"] == store_id

    def test_normal_account_cant_list_his_stores(self):
        self.client.force_login(self.normal_account)
        res = self.client.get(self.resolve_url("stores-me"))
        assert res.json() == []

    def test_account_get_all_stores(self):
        self.client.post(self.url, self.payload)
        self.payload["name"] = "tt"
        res = self.client.post(self.url, self.payload)
        store = Store.objects.get(id=res.json()["id"])
        store.is_active = False
        res = self.client.get(self.resolve_url("stores-me"))
        stores = res.json()["results"]
        assert len(stores) == 2

    def test_store_delete(self):
        self.client.force_login(self.account)
        res = self.client.post(self.url, self.payload)
        store_id = res.json()["id"]
        response = self.client.delete(self.resolve_url("stores-detail", pk=store_id))
        assert response.status_code == 204
        store = Store.objects.filter(id=store_id).first()
        assert store.is_active is False

    def test_deactivate_account_deactivate_stores(self):
        self.client.post(self.url, self.payload)
        self.payload["name"] = "test"
        self.client.post(self.url, self.payload)
        self.account.deactivate()
        self.account.deactivate()
        stores = Store.objects.filter(owner=self.account)
        for store in stores:
            assert store.is_active is False
            assert store.deactivate_date is not None
