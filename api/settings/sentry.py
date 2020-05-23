from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

branch = os.environ.get("GIT_BRANCH", "ref/head/local")[11:]
sha_commit = os.environ.get("SHA_COMMIT", "null commit")[:7]

sentry_sdk.init(
    dsn=get_env("SENTRY_URL"),
    integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
    send_default_pii=True,
    release=f"{branch}-{sha_commit}"
)
