from .base import *
from config.celery import app

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / 'db.sqlite3'),
    }
}

CELERY_TASK_ALWAYS_EAGER = True
