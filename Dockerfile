FROM python:3.8.2-alpine3.11

RUN mkdir /code /code/scripts && \
    apk add  jpeg-dev zlib-dev libmagic && \
    apk add --no-cache --virtual build-deps gcc build-base musl-dev curl jpeg-dev zlib-dev libffi-dev && \
    apk add postgresql-dev && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH="/root/.poetry/bin:$PATH"

WORKDIR /code

COPY ./pyproject.toml .

COPY ./poetry.lock .

RUN poetry config virtualenvs.in-project true && \
    poetry install
    
RUN apk del build-deps 

COPY ./api .

COPY ./scripts ./scripts

RUN poetry run python manage.py collectstatic --noinput --settings=settings.build

RUN chmod +x scripts/run_server.sh

ARG GITHUB_SHA
ENV SHA_COMMIT $GITHUB_SHA

ARG GITHUB_REF
ENV GIT_BRANCH $GITHUB_REF

CMD sh scripts/run_server.sh