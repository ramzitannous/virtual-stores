from .base import *
from config.celery import app

DEBUG = True

CELERY_TASK_ALWAYS_EAGER = True
