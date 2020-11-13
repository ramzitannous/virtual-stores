import logging
from accounts.views import AccountViewSet, SocialLoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from stores.views import StoreViewMixin, StoreReviewDeleteView, StoreReviewListCreateView
from products.views import CategoryListView, ProductViewSet, \
    ProductReviewListCreateView, ProductReviewDeleteView
v1_router = DefaultRouter()

# accounts
v1_router.register("accounts", AccountViewSet, basename="accounts")

# stores
v1_router.register('stores', StoreViewMixin, basename="stores")
v1_router.register("stores/reviews", StoreReviewDeleteView, basename="stores-review")
v1_router.register(r"stores/(?P<store_id>[^/]+)/reviews", StoreReviewListCreateView, basename="stores-review")

# products & categories
v1_router.register("categories", CategoryListView, basename="categories")
v1_router.register("products", ProductViewSet, basename="products")
v1_router.register("products/reviews", ProductReviewDeleteView, basename="products-review")
v1_router.register(r"products/(?P<product_id>[^/]+)/reviews", ProductReviewListCreateView, basename="products-review")

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path("social", SocialLoginView.as_view(), name="social-login")
] + v1_router.urls

logger = logging.getLogger("stores.urls")

if settings.DEBUG:
    for url in urlpatterns:
        logger.debug(url)
