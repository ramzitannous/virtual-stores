from __future__ import absolute_import
from settings.base import get_env
from celery import Celery
from celery.bin.purge import purge

app = Celery('Stores')

app.conf.ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': get_env("REDIS_URL"),
    'default_timeout': 60 * 60
  }
}
app.conf.timezone = 'Asia/Jerusalem'
purge(app)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
