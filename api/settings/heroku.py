from .prod import *

MIDDLEWARE += ("whitenoise.middleware.WhiteNoiseMiddleware",)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
