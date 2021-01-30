poetry install && \
cd api && \
poetry run python manage.py migrate --settings=settings.test && \
poetry run python manage.py test --settings=settings.test --no-input && \
rm -r ../media