from .sentry import *
import dj_database_url

DEBUG = False

DATABASES['default'] = dj_database_url.config(default=get_env("DATABASE_URL"), conn_max_age=600)

SECRET_KEY = get_env("SECRET_KEY")

ALLOWED_HOSTS = [get_env("DOMAIN_NAME")]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_FRAME_DENY = True
SECURE_SSL_REDIRECT = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

