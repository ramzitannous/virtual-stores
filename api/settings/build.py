import json
import os
import pathlib

from google.oauth2 import service_account

from shared.utils import get_env

SECRET_KEY = "build"

BASE_DIR = pathlib.Path(os.path.dirname(__file__)).parent

STATIC_URL = "/static/"
STATIC_ROOT = "static"

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = get_env('GS_BUCKET_NAME')
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
    json.loads(get_env("GS_CREDENTIALS"))
)

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
