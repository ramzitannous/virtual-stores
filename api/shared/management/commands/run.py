import multiprocessing
import os
from argparse import ArgumentParser

from django.core.management import BaseCommand

from shared.utils import get_env

CELERY_THREADS = os.environ.get("CELERY_THREADS", 5)
COMMANDS = ("worker", "beat", "server", "flower", "createadmin", "waitdb")


class Command(BaseCommand):
    help = "run app commands"

    @staticmethod
    def run_worker():
        os.system(
            f'celery worker -A config -l info -P threads  -c {CELERY_THREADS} --without-gossip --heartbeat-interval 5 -E --purge')

    @staticmethod
    def run_beat():
        if os.path.exists('celerybeat.pid'):
            os.remove('celerybeat.pid')
        os.system('celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler')

    @staticmethod
    def run_server():
        port = os.environ.get("PORT", 8000)
        cpu_count = (multiprocessing.cpu_count() * 2) + 1
        os.system(
            f'gunicorn -b 0.0.0.0:{port} -w {cpu_count} -k uvicorn.workers.UvicornWorker config.asgi:application --preload')

    @staticmethod
    def run_flower():
        os.system(f'celery flower -A config --basic_auth={get_env("ADMIN_EMAIL")}:{get_env("ADMIN_PASSWORD")}\
               --address=0.0.0.0 --port=5555')

    @staticmethod
    def run_waitdb():
        from scripts.wait_db import pg_isready
        pg_isready()

    @staticmethod
    def run_createadmin():
        from scripts.setup import create_admin
        create_admin()

    def add_arguments(self, parser: ArgumentParser):
        for cmd in COMMANDS:
            parser.add_argument(f"--{cmd}", action='store_true')

    def handle(self, *args, **options):
        for command in COMMANDS:
            if options[command]:
                self.stdout.write(f"Running command {command} ...")
                run_command = getattr(Command, f"run_{command}")
                run_command()
                self.stdout.write(f"Command {command} run successfully ...")
                break
