if [ "${DJANGO_SETTINGS_MODULE}" == "settings.local" ]; then
    poetry run python manage.py migrate && \
    poetry run python manage.py createadmin
    poetry run python manage.py runserver 0.0.0.0:"${PORT}"
    
else
    poetry run python manage.py waitdb && \
    poetry run python manage.py migrate && \
    poetry run python manage.py createadmin && \
    poetry run python manage.py runbackend
fi