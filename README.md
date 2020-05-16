
# Stores Backend  
![Build and Deploy Backend](https://github.com/Stores2020/backend/workflows/Build%20and%20Deploy%20Backend/badge.svg?branch=master)

**Setup Guide**

 1. Install poetry
[https://python-poetry.org/docs/](https://python-poetry.org/docs/)

 2. Install depencies

    `poetry config virtualenvs.in-project true && 
 poetry install --no-dev`
 
 3.  create .env file



| Name | required |
|--|--|
| DATABASE_URL | false |
| SENTRY_URL | false |
|REDIS_URL| false|
|SECRET_KEY| true ( can be anything)|
|ENABLE_EMAIL|  true (0)|
|EMAIL_HOST| false|
|EMAIL_PORT| false|
|EMAIL_HOST_USER| false|
|EMAIL_HOST_PASSWORD| false|
|DEFAULT_FROM_EMAIL| false
|DOMAIN_NAME| false|
|ADMIN_EMAIL| true|
|ADMIN_PASSWORD|true|

 4. Create local admin using ADMIN_EMAIL, ADMIN_PASSWORD:
 `python manage.py createadmin`

5. run migrations
`python manage.py migrate`


**Commands**
| command | use  |
|--|--|
|`python manage.py runbackend`  | run gunicorn production server |
|`python manage.py runbeat`  | run celery beat schedulare |
|`python manage.py runworker`  | run celery worker |
|`python manage.py runflower`  | run celery flower monitoring |
|`python manage.py createadmin`  | create local super admin |
|`python manage.py waitdb`  | wait for database to be ready |


**Deployment**
1. Heroku Deploy check .github folder
