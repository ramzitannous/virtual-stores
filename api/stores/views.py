from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, \
    DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from stores.models import Store, StoreReview
from stores.serializers import StoreSerializer, StoreReviewSerializer
from stores.permissions import StorePermissions


class StoreViewMixin(GenericViewSet,
                     CreateModelMixin, RetrieveModelMixin, ListModelMixin,
                     DestroyModelMixin, UpdateModelMixin):
    serializer_class = StoreSerializer
    queryset = Store.objects.select_related("address", "owner").all()
    permission_classes = [StorePermissions]


class StoreReviewDeleteView(GenericViewSet, DestroyModelMixin):
    queryset = StoreReview.objects.all()
    permission_classes = [StorePermissions]


class StoreReviewListCreateView(GenericViewSet, CreateModelMixin, ListModelMixin):
    permission_classes = [StorePermissions]
    serializer_class = StoreReviewSerializer

    def get_queryset(self):
        return StoreReview.objects.select_related("owner")\
            .filter(store_id=self.kwargs.get("store_id"))

    def create(self, request, *args, **kwargs):
        review_serializer = StoreReviewSerializer(data=request.data)
        review_serializer.is_valid(raise_exception=True)
        store = get_object_or_404(Store, id=self.kwargs.get("store_id"))
        review = StoreReview.objects.create(**review_serializer.validated_data, store=store, owner=self.request.user)
        response_serializer = StoreReviewSerializer(review)
        return Response(response_serializer.data, status=201)

