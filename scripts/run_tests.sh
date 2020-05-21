pip install -r requirements.txt && \
cd api && \
python manage.py waitdb && \
python manage.py migrate --settings=settings.test && \
python manage.py test --settings=settings.test && \
rm -r media