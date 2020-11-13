
**Virtual Stores API Server** 

The idea for the project is that store owners can open virtual stores to show their products with images & description, then users can add reviews and buy them.    
    
[https://stores2020.herokuapp.com/swagger](https://stores2020.herokuapp.com/swagger)    
    
[http://stores2020.herokuapp.com/admin](http://stores2020.herokuapp.com/admin)    
     
    
![Build and Deploy Backend](https://github.com/Stores2020/backend/workflows/Build%20and%20Deploy%20Backend/badge.svg?branch=master)      
            
***Project contains python, [django](https://www.djangoproject.com/) and [django-rest-framework](https://www.django-rest-framework.org/)  best practices***    
1. Multiple environments (dev, build, prod, testing, heroku)     
 2. Python Package Management using [python-poetry](https://python-poetry.org/)    
 3. Container based deployment using docker & docker-compose    
 4. Project configuration using environment variables  [python-dotenv](https://pypi.org/project/python-dotenv/)    
 5. Ability to handle high loads of concurrent requests using [uvicorn](https://github.com/encode/uvicorn) that implements  [uvloop](https://github.com/MagicStack/uvloop) (Ultra fast asyncio event loop) to handle high loads     
 6. Unit & integration testing with mocked DB objects using [django-factory_boy](https://github.com/FactoryBoy/django-factory_boy) and [pytest](https://github.com/pytest-dev/pytest)    
 7. User Management and Authentication  [djoser](https://github.com/sunscrapers/djoser) and [django-rest-framework-simplejwt](https://github.com/SimpleJWT/django-rest-framework-simplejwt)    
 8. Social Login to Google & Facebook using   [social-app-django](https://github.com/python-social-auth/social-app-django)
 9. Image thumbnails using [django-versatileimagefield](https://github.com/respondcreate/django-versatileimagefield)
10. Distributed Queues & Background processing using [celery](https://github.com/celery/celery) and [redis](https://pypi.org/project/redis/)    
11. Scheduled Jobs using [django-celery-beat](django-celery-beat) and [celery](https://github.com/celery/celery)    
12. Celery monitoring using [flower](https://github.com/mher/flower)    
13. API documentaion using [drf-yasg](https://github.com/axnsan12/drf-yasg)    
14. Exception &  Error reporting using [sentry](https://docs.sentry.io/platforms/python/guides/django/)    
15. Relation and API filtering using [django-filter](https://github.com/carltongibson/django-filter)    
16. Cloud storage for static files using [django-storages](https://django-storages.readthedocs.io/en/latest/index.html)    
17. CI/CD and Test Runner using [Github Actions](https://docs.github.com/en/free-pro-team@latest/actions)     
18. shared app that contains base models & classes for other apps,    
19. run commands using django BaseCommand  
  
  **UML Diagram**
  ![DB Image](https://raw.githubusercontent.com/ramzitannous/virtual-stores/master/db_uml.png?token=AFHYIN4Y4TY4ZIAKMU5MFEK7XAH6Q)
 **Setup Guide** 
 1. Install poetry              
[https://python-poetry.org/docs/](https://python-poetry.org/docs/)              
              
 2. Install dependances              
              
    `poetry config virtualenvs.in-project true && poetry install` 3. create .env file              
                          
              
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
|GOOGLE_KEY|false|      
|GOOGLE_SECRET|false|      
|FACEBOOK_KEY|false|      
|FACEBOOK_SECRET| false|       
 4. install postgres db or run it from docker-compose          
  `docker-compose -f docker-compose.local.yaml -p stores up -d db` 5. login to  postgres database            
  `psql postgres -h localhost -p 5432 -U postgres -W` 6. create stores database            
   ` CREATE DATABASE stores;` 7. Create local admin using ADMIN_EMAIL, ADMIN_PASSWORD:              
 `python manage.py run --createadmin` 8. run migrations              
`python manage.py migrate`              
              
 **Commands**         
 | command | use  |              
|--|--|              
|`python manage.py run --server` | run gunicorn production server |              
|`python manage.py run --beat` | run celery beat schedulare |              
|`python manage.py run --worker` | run celery worker |              
|`python manage.py run --flower` | run celery flower monitoring |              
|`python manage.py run --createadmin` | create local super admin |              
|`python manage.py run --waitdb` | wait for database to be ready |              
              
              
**Deployment**
 1. Heroku Deploy check .github folder
