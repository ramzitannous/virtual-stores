from config.celery import app
from .prod import *

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE += ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE + ["whitenoise.middleware.WhiteNoiseMiddleware"]

CORS_ORIGIN_ALLOW_ALL = True
