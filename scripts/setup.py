import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
import django
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

TEST_EMAIL = "admin@admin.com"
TEST_PASSWORD = "admin@123"


def create_admin():
    print("\n")
    print("\n")
    print("----------------------------------------------------------------------------------")
    User: AbstractUser = get_user_model()
    user, created = User.objects.get_or_create(email=TEST_EMAIL, is_superuser=True, is_staff=True)
    if created:
        user.set_password(TEST_PASSWORD)
        user.save()
        print(f"created admin .........")
    else:
        print("admin already created ....")

    print(f"Password: {TEST_PASSWORD}")
    print(f"Email: {TEST_EMAIL}")
    print("----------------------------------------------------------------------------------")
    print("\n")
    print("\n")