import logging
from time import time, sleep
import psycopg2
from settings.base import get_env
import dj_database_url

TIMEOUT = 30
INTERVAL = 1


db = dj_database_url.parse(get_env("DATABASE_URL"))

config = {
    "dbname": db["NAME"],
    "user": db["USER"],
    "password": db["PASSWORD"],
    "host": db["HOST"],
    "port": db["PORT"]
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