import os
import pathlib

SECRET_KEY = "build"

BASE_DIR = pathlib.Path(os.path.dirname(__file__)).parent

STATIC_URL = "/static/"
STATIC_ROOT = "static"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "versatileimagefield",
    "drf_yasg"
]
