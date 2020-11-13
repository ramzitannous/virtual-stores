if [ "${DJANGO_SETTINGS_MODULE}" == "settings.local" ]; then
    poetry run python manage.py migrate && \
    poetry run python manage.py run --createadmin
    poetry run python manage.py runserver 0.0.0.0:"${PORT}"
    
else
    poetry run python manage.py run --waitdb && \
    poetry run python manage.py migrate && \
    poetry run python manage.py run --createadmin && \
    poetry run python manage.py run --server
fi