from shared.tests import BaseTestCase
from stores.models import Store
from users.models import CustomUser


class TestStoreCreate(BaseTestCase):
    payload = {
        "name": "Test Store",
        "description": "test description",
        "phone": "asdfasdf",
        "open_time": "12:00:PM",
        "close_time": "12:00:PM",
        "address": {
            "city": "ramallah",
            "street": "batten al hawa",
            "extra": "near"
        }
    }

    def setUp(self) -> None:
        super().setUp()
        self.url = self.resolve_url("stores-list")

    def test_create_store_authenticated(self):
        response = self.client.post(self.url, self.payload)
        assert response.data is not None
        assert response.status_code == 201
        Store.objects.get(id=response.data["id"]).delete()

    def test_create_store_not_authenticated(self):
        self.client.logout()

        response = self.client.post(self.url, self.payload)
        assert response.status_code == 401

    def test_list_unauthenticated(self):
        response = self.client.post(self.url, self.payload)
        self.client.logout()
        list_response = self.client.get(self.url)
        assert list_response.status_code == 200
        assert len(list_response.data["results"]) == 1
        Store.objects.get(id=response.data["id"]).delete()

    def test_allow_update_store(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.payload)
        _id = response.data["id"]
        res = self.client.patch(self.resolve_url("stores-detail", pk=_id), {"name": "test"})
        assert res.status_code == 200

    def test_deny_update_store(self):
        response = self.client.post(self.url, self.payload)
        self.client.logout()
        user = CustomUser.objects.create(email="ramzi", password="451")
        self.client.force_login(user)
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

    def test_prevent_delete_by_other_user(self):
        res = self.client.post(self.url, self.payload)
        self.client.logout()
        user = CustomUser.objects.create(email="ramzi", password="451")
        self.client.force_login(user)
        response = self.client.delete(self.resolve_url("stores-detail", pk=res.data["id"]))
        assert response.status_code == 403

    def test_add_a_comment(self):
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
        assert reviews[0]["owner"]["id"] == str(self.user.id)
        assert reviews[0]["owner"]["fullName"] == str(self.user.get_full_name())

    def test_prevent_delete_comment_by_other_user(self):
        res = self.client.post(self.url, self.payload)
        store_id = res.json()["id"]
        url = self.resolve_url("stores-review-list", store_id=res.json()["id"])
        res = self.client.post(self.resolve_url("stores-review-list", store_id=store_id), {
            "title": "hello",
            "rating": 5
        })
        self.client.logout()
        user = CustomUser.objects.create(email="ramzi", password="451")
        self.client.force_login(user)
        response = self.client.delete(self.resolve_url("stores-review-detail", pk=res.data["id"]))
        assert response.status_code == 403
