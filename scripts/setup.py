import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
import django
django.setup()

from accounts.enums import AccountTypes, AccountStatus
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from settings.base import get_env

ADMIN_EMAIL = get_env("ADMIN_EMAIL")
ADMIN_PASSWORD = get_env("ADMIN_PASSWORD")


def create_admin():
    print("\n")
    print("\n")
    print("----------------------------------------------------------------------------------")
    User: AbstractUser = get_user_model()
    user, created = User.objects.get_or_create(email=ADMIN_EMAIL, is_superuser=True,
                                               is_staff=True, first_name="Stores",
                                               last_name="Admin", type=AccountTypes.BUSINESS)
    user.status = AccountStatus.VERIFIED,
    user.on_trial = False
    user.is_active = True
    user.save()

    if created:
        user.set_password(ADMIN_PASSWORD)
        user.save()
        print(f"created admin .........")
    else:
        print("admin already created ....")

    print(f"Password: {ADMIN_EMAIL}")
    print(f"Email: {ADMIN_PASSWORD}")
    print("----------------------------------------------------------------------------------")
    print("\n")
    print("\n")


create_admin()
