from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration


sentry_sdk.init(
    dsn=get_env("SENTRY_URL"),
    integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
    send_default_pii=True
)
