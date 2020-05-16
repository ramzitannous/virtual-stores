#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import multiprocessing
import os
import sys
from shared.utils import get_env
import dotenv

dotenv.load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
CELERY_THREADS = os.environ.get("CELERY_THREADS", 5)


def main():
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    arg = sys.argv[1]
    if arg == 'runworker':
        os.system(
            f'celery worker -A config -l info -P threads  -c {CELERY_THREADS} --without-gossip --heartbeat-interval 5 -E --purge')

    elif arg == 'runbeat':
        if os.path.exists('celerybeat.pid'):
            os.remove('celerybeat.pid')
        os.system('celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler')

    elif arg == 'runbackend':
        port = os.environ.get("PORT", 8000)
        cpu_count = (multiprocessing.cpu_count() * 2) + 1
        os.system(f'gunicorn -b 0.0.0.0:{port} -w {cpu_count} -k gthread config.wsgi:application --preload')

    elif arg == 'runflower':
        os.system(f'celery flower -A config --basic_auth={get_env("ADMIN_EMAIL")}:{get_env("ADMIN_PASSWORD")}\
         --address=0.0.0.0 --port=5555')

    elif arg == "createadmin":
        from scripts.setup import create_admin
        create_admin()

    elif arg == "waitdb":
        from scripts.wait_db import pg_isready
        pg_isready()

    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
