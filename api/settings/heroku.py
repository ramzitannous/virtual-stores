from .prod import *

MIDDLEWARE += ("whitenoise.middleware.WhiteNoiseMiddleware",)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE += ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE

CORS_ORIGIN_ALLOW_ALL = True
