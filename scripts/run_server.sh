if [ "${DJANGO_SETTINGS_MODULE}" == "settings.prod" ]; then
    poetry run python scrips/wait_db.py && \
    poetry run python manage.py migrate && \
    poetry run python manage.py createadmin && \
    poetry run python manage.py runbackend
else
    poetry run python manage.py migrate && \
    poetry run python manage.py createadmin
    poetry run python manage.py runserver 0.0.0.0:"${PORT}"
fi