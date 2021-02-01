from typing import List

import click
from pathlib import Path

import sys

from faker.generator import random

BASE_DIR = Path(__file__).resolve().parent.parent / 'api'
sys.path.append(str(BASE_DIR.absolute()))

import django

django.setup()

from accounts.models import Account
from accounts.enums import AccountTypes, Gender, AccountStatus
from stores.models import Store, StoreAddress, StoreReview
from products.models import Product, ProductImage, Category, ProductReview
from products.enum import ProductSize
from faker import Faker
from django.core.files import File

fake = Faker()

IMG_DIR = Path(".") / 'fake_images'

REVIEWS = (
    ("Very Bad", 1),
    ("Bad", 2),
    ("Good", 3),
    ("Very Good", 4),
    ("Excellent", 5),
)


def print_ids(objs: list):
    for i, obj in enumerate(objs):
        print(f"{i} - {obj.id}")


def generate_accounts(count=1):
    print(f'generating {count} account(s) ...')
    accounts_arr = []
    for _ in range(count):
        fake_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "address": None,
            "phone": fake.phone_number(),
            "type": AccountTypes.BUSINESS,
            "status": AccountStatus.VERIFIED,
            "gender": Gender.M,
            "is_active": True,
            "on_trial": False,
            "email": fake.email()
        }
        account = Account(**fake_data)
        account.image.save("profile", File(open(IMG_DIR / 'profile.png', "rb")))
        account.save()
        accounts_arr.append(account)
    print(f"end generating accounts")
    return accounts_arr


def generate_store(account_id: str, count=1):
    print(f'generating {count} store for {account_id} ...')
    account = Account.objects.get(id=account_id)
    stores = []
    for _ in range(count):
        store_data = {
            "name": fake.company(),
            "description": fake.catch_phrase(),
            "phone": fake.msisdn(),
            "open_time": fake.time("%H:%M:%p"),
            "close_time": fake.time("%H:%M:%p"),
        }
        address = {
            "city": fake.city(),
            "street": fake.street_name(),
            "extra": fake.street_address()
        }

        store = Store(owner=account, **store_data)
        address = StoreAddress.objects.create(**address)
        store.address = address
        store.image.save("store", File(open(IMG_DIR / "store.png", "rb")))
        store.save()
        stores.append(store)
    print(f"end generating stores")
    return stores


def generate_reviews(owner_id: str, model, _id: str, count=1):
    print(f"generating {count} review for {_id}")
    account = Account.objects.get(id=owner_id)
    reviews = []
    for _ in range(count):
        i = random.randint(0, 4)
        review = model(title=REVIEWS[i][0], rating=REVIEWS[i][1], owner=account)
        reviews.append(review)
    return reviews


def generate_products(store_id: str, count=1) -> List[Product]:
    print(f"generating {count} products for store {store_id}")
    store = Store.objects.select_related("owner").get(id=store_id)
    category, _ = Category.objects.get_or_create(name="Clothing")
    products_img = IMG_DIR / 'products'
    _products = []
    for _ in range(count):
        for p in products_img.iterdir():
            product = Product()
            product.name = p.name
            product.description = f"{p.name} dummy product"
            product.price = fake.random.randint(10, 200)
            product.store = store
            product.sizes = [ProductSize.M, ProductSize.L, ProductSize.XL, ProductSize.XXL]
            sizes = []
            for _ in range(3):
                sizes.append(fake.random.randint(40, 45))
            product.integer_sizes = sizes
            colors = []
            for _ in range(5):
                colors.append(fake.color_name())
            product.colors = colors
            product.category = category
            product.quantity = random.randint(10, 50)
            product.owner = store.owner
            product.save()
            for img in p.iterdir():
                product_img = ProductImage()
                product_img.product = product
                product_img.image.save(f"{p.name}-{img.name}",
                                       File(open(str(img.absolute()), "rb")))
                product.save()
            _products.append(product)
        return _products


#########################################################################
# commands
#########################################################################


@click.group()
def cli():
    pass


@cli.command(help="generate accounts")
@click.argument("count", type=int)
def accounts(count: int):
    acc = generate_accounts(count)
    print_ids(acc)


@cli.command("store", help="generate store for owner")
@click.argument("account_id", type=str)
@click.argument("count", type=int)
def store_cli(account_id: str, count: int):
    stores = generate_store(account_id, count)
    print_ids(stores)


@cli.command("store-review", help="generate reviews for store")
@click.argument("store_id", type=str)
@click.argument("count", type=int)
@click.argument("owner", type=str)
def store_reviews(store_id: str, count: int, owner: str):
    reviews = generate_reviews(owner, StoreReview, store_id, count)
    store = Store.objects.get(id=store_id)
    for review in reviews:
        review.store = store
        review.save()


@cli.command(help="generate products for store")
@click.argument("store_id", type=str)
@click.argument("count", type=int)
def products(store_id: str, count: int):
    generate_products(store_id, count)


@cli.command("product-review", help="generate reviews for product")
@click.argument("product_id", type=str)
@click.argument("count", type=int)
@click.argument("owner", type=str)
def product_reviews(product_id: str, count: int, owner: str):
    reviews = generate_reviews(owner, ProductReview, product_id, count)
    product = Product.objects.get(id=product_id)
    for review in reviews:
        review.product = product
        review.save()


@cli.command("generate_data", help="generate data")
@click.argument("count", type=int)
def generate_data(count: int):
    _accounts = generate_accounts(count)
    for account in _accounts:
        stores = generate_store(account.id, 5)
        for store in stores:
            _products = generate_products(store.id, 30)
            for product in _products:
                generate_reviews(account.id, ProductReview, product.id, 2)


if __name__ == "__main__":
    cli.add_command(accounts)
    cli()
