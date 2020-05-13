import logging

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from stores.views import StoreViewMixin, StoreReviewDeleteView, StoreReviewListCreateView

v1_router = DefaultRouter()

# stores
v1_router.register('stores', StoreViewMixin, basename="stores")
v1_router.register("stores/reviews", StoreReviewDeleteView, basename="stores-review")
v1_router.register(r"stores/(?P<store_id>[^/]+)/reviews", StoreReviewListCreateView, basename="stores-review")

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
] + v1_router.urls

logger = logging.getLogger("store.urls")

if settings.DEBUG:
    for url in urlpatterns:
        logger.info(url)