"""
ASGI config for api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
import dotenv

dotenv.load_dotenv()

application = get_asgi_application()
