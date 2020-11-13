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
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
