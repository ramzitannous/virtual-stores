from .sentry import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env("DB_NAME"),
        'USER': get_env("DB_USER"),
        'PASSWORD': get_env("DB_PASSWORD"),
        'HOST': get_env("DB_HOST"),
        'PORT': get_env("DB_PORT")
    }
}

SECRET_KEY = get_env("SECRET_KEY")

ALLOWED_HOSTS = [get_env("DOMAIN")]
