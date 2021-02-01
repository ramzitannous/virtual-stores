from config.celery import app
from .prod import *

CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE += ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE

CORS_ORIGIN_ALLOW_ALL = True
