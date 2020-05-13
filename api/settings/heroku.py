from .prod import *
import dj_database_url

DATABASES['default'] = dj_database_url.config(default=get_env("DATABASE_URL"), conn_max_age=600)