from __future__ import absolute_import

from celery import Celery
from celery.bin.purge import purge

app = Celery('Stores')

app.conf.timezone = 'Asia/Jerusalem'
app.conf.lock_timeout = 90 * 60
purge(app)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
