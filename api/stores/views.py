from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, \
    DestroyModelMixin
from shared.permissions import BUSINESS_PERMISSIONS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from stores.models import Store, StoreReview
from stores.serializers import StoreSerializer, StoreReviewSerializer


class StoreViewMixin(ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.select_related("address", "owner") \
        .annotate(reviews_avg=Avg("reviews__rating"), reviews_count=Count("reviews")) \
        .filter(is_active=True)
    permission_classes = BUSINESS_PERMISSIONS
    ordering_fields = ("reviews_avg",)
    filterset_fields = ("address__city", "name")

    @action(methods=["get"], detail=False, description="get my stores")
    def me(self, *args, **kwargs):
        self.queryset = self.queryset.filter(is_active__in=[True, False], owner=self.request.user)
        return self.list(*args, **kwargs)


class StoreReviewDeleteView(GenericViewSet, DestroyModelMixin):
    queryset = StoreReview.objects.all()


class StoreReviewListCreateView(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = StoreReviewSerializer

    def get_queryset(self):
        return StoreReview.objects.select_related("owner") \
            .filter(store_id=self.kwargs.get("store_id"))

    def create(self, request, *args, **kwargs):
        review_serializer = self.serializer_class(data=request.data)
        review_serializer.is_valid(raise_exception=True)
        store = get_object_or_404(Store, id=self.kwargs.get("store_id"))
        review = StoreReview.objects.create(**review_serializer.validated_data, store=store, owner=self.request.user)
        response_serializer = self.serializer_class(review)
        return Response(response_serializer.data, status=201)
