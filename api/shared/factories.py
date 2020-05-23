from factory.django import DjangoModelFactory
from accounts.models import Account
import factory
from accounts.enums import AccountTypes, AccountStatus
from products.models import Category, Product
from stores.models import Store, StoreAddress


class OwnerFactory(DjangoModelFactory):
    class Meta:
        model = Account

    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    email = factory.Faker("email")
    type = AccountTypes.BUSINESS
    status = AccountStatus.VERIFIED
    phone = factory.Faker("phone_number")


class BusinessAccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    email = factory.Faker("email")
    type = AccountTypes.BUSINESS
    status = AccountStatus.VERIFIED
    phone = factory.Faker("phone_number")
    on_trial = False


class NormalAccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    email = factory.Faker("email")
    type = AccountTypes.NORMAL
    status = AccountStatus.VERIFIED
    on_trial = False
    phone = factory.Faker("phone_number")


class TrialAccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    email = factory.Faker("email")
    type = AccountTypes.BUSINESS
    status = AccountStatus.VERIFIED
    on_trial = True
    phone = factory.Faker("phone_number")


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = StoreAddress

    city = "Test City"
    street = "Test Street"
    extra = "Test Extra"


class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.Faker("name")
    open_time = "12:00:PM"
    close_time = "12:00:PM"
    owner = factory.SubFactory(OwnerFactory)
    is_active = True
    address = factory.SubFactory(AddressFactory)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("name")
    description = factory.Faker("name")
    category = factory.SubFactory(CategoryFactory)
    price = 10
    owner = factory.SubFactory(OwnerFactory)
    store = factory.SubFactory(StoreFactory)
    quantity = 10
    extras = {
        "brand": "addidas"
    }
