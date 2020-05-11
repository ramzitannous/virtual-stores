"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, include
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import SessionAuthentication
from shared import views as ping_view

schema_view = get_schema_view(
    openapi.Info(
        title='Store API',
        default_version='v1',
        description="Store Management Backend",
    ),
    public=True,
    authentication_classes=(SessionAuthentication,),
    permission_classes=()
)

urlpatterns = [
    re_path(r'^admin/?', admin.site.urls),
    re_path(r'^ping/?', ping_view.ping, name='ping_view'),
    re_path(r'^auth/', include('rest_framework.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
    re_path(r'^api/(?P<version>(v1))/', include('config.api_v1_urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)