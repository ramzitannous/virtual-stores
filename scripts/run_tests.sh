pip install -U pip &&
pip install -r requirements.txt && \
cd api && \
python manage.py migrate --settings=settings.test && \
python manage.py test --settings=settings.test --np-input && \
rm -r media