import json

from .sentry import *
from google.oauth2 import service_account

DEBUG = False

SECRET_KEY = get_env("SECRET_KEY")

ALLOWED_HOSTS = [get_env("DOMAIN_NAME")]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_FRAME_DENY = True
SECURE_SSL_REDIRECT = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = get_env('GS_BUCKET_NAME')
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
    json.loads(get_env("GS_CREDENTIALS"))
)
