from .sentry import *
import dj_database_url

DEBUG = False

DATABASES['default'] = dj_database_url.config(default=get_env("DATABASE_URL"), conn_max_age=600)

SECRET_KEY = get_env("SECRET_KEY")

ALLOWED_HOSTS = [get_env("DOMAIN_NAME")]
