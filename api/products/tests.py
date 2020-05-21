import os

from django.test.client import encode_multipart
from products.models import Product, ProductReview, ProductImage
from shared.tests import BaseTestCase
from shared.factories import StoreFactory, CategoryFactory, ProductFactory
from django.conf import settings


class Tests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.parent1 = CategoryFactory()
        self.parent2 = CategoryFactory()
        self.child1 = CategoryFactory(parent=self.parent1)
        self.child2 = CategoryFactory(parent=self.parent1)
        self.cat_url = self.resolve_url("categories-list")
        self.product_url = self.resolve_url("products-list")
        self.cat = CategoryFactory()
        self.store = StoreFactory()

        self.product_data = {
            "name": "test product",
            "category_id": str(self.cat.id),
            "store_id": str(self.store.id),
            "price": 10,
            "desc": "radsa",
            "colors": ["red", "green"],
            "sizes": ["S", "M", "XXL"],
            "integer_sizes": [10, 20],
            "quantity": 20,
            "extras": {
                "brand": "addidas",
                "material": "cotton"
            }
        }

    def test_list_categories(self):
        result = self.client.get(self.cat_url)
        cats = result.json()["results"]
        assert len(cats) == 3

    def test_list_subcategories(self):
        url = self.resolve_url("categories-subcategories", pk=str(self.parent1.id))
        result = self.client.get(url)
        assert result.status_code == 200
        cats = result.json()["results"]
        cats[0]["parent"] = str(self.parent1.id)
        assert len(cats) == 2

    def test_product_create(self):
        res = self.client.post(self.product_url, self.product_data)
        product_data = res.json()
        assert res.status_code == 201
        product = Product.objects.get(id=product_data["id"])
        assert product.store_id == self.store.id
        assert product.category_id == self.cat.id
        assert product.owner_id == self.account.id
        product.delete()

    def test_add_review(self):
        product = ProductFactory()
        url = self.resolve_url("products-review-list", product_id=product.id)
        res = self.client.post(url, {
            "title": "good",
            "rating": 4
        })
        res = self.client.post(url, {
            "title": "good",
            "rating": 5
        })
        assert res.status_code == 201
        _id = res.json()["id"]
        review = ProductReview.objects.select_related("owner", "product").get(id=_id)
        assert review.owner.id == self.account.id
        assert review.product.id == product.id

        products_url = self.resolve_url("products-list")
        res = self.client.get(products_url)
        assert res.status_code == 200
        stores = res.json()
        assert stores["results"][0]["reviewsCount"] == 2
        assert stores["results"][0]["reviewsAvg"] == 4.5
        product.delete()

    def test_upload_images(self):
        product = ProductFactory(owner=self.account)
        images = []
        image_names = ["placeholder60x60.png", "placeholder120x120.png"]
        for img in image_names:
            images.append(self.get_image(img))

        url = self.resolve_url("products-upload-images", pk=str(product.id))
        res = self.client.post(url, {"images": images})
        assert res.status_code == 200
        product_image = ProductImage.objects.filter(product=product)
        assert product_image.count() == 2
        products = self.client.get(self.product_url).json()["results"]
        assert len(products[0]["images"]) == 2
        product_image = ProductImage.objects.filter(product=product).first()
        url = self.resolve_url("products-image", pk=product.id, image_id=product_image.id)
        res = self.client.delete(url)
        assert res.status_code == 204
        assert ProductImage.objects.filter(product=product).count() == 1
        for img in ProductImage.objects.filter(product=product):
            img.image.delete()

    def test_create_discount(self):
        product = ProductFactory(price=10)
        product.create_discount(0.2)
        assert product.discount_price == 8
        assert product.on_discount

    def tearDown(self) -> None:
        self.child1.delete()
        self.child2.delete()
        self.parent1.delete()
        self.parent2.delete()
        super().tearDown()
