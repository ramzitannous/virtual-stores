import logging
from time import time, sleep
import psycopg2
from settings.base import get_env

TIMEOUT = 30
INTERVAL = 1


config = {
    "dbname": get_env("DB_NAME"),
    "user": get_env("DB_USER"),
    "password": get_env("DB_PASSWORD"),
    "host": get_env("DB_HOST"),
    "port": get_env("DB_PORT")
}

start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def pg_isready():
    while time() - start_time < TIMEOUT:
        try:
            conn = psycopg2.connect(**config)
            logger.info("Postgres is ready! ✨ 💅")
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info(f"Postgres isn't ready. Waiting for {INTERVAL} seconds ...")
            sleep(INTERVAL)

    logger.error(f"We could not connect to Postgres within {TIMEOUT} seconds.")
    return False


pg_isready()