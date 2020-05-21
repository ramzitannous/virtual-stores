from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from products.models import Category, Product, ProductReview, ProductImage
from products.serializers import CategorySerializer, ProductGetSerializer, ProductCreateSerializer, \
    ProductReviewSerializer, ProductCreateImageSerializer


class CategoryListView(GenericViewSet, ListModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(parent=None)
    ordering_fields = ["name"]

    @action(methods=["get"], detail=True)
    def subcategories(self, request, *args, **kwargs):
        parent_category = get_object_or_404(Category, id=self.kwargs["pk"])
        self.queryset = Category.objects.filter(parent=parent_category)
        return self.list(request, args, kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related("images").select_related("category", "store", "owner") \
        .filter(is_active=True).annotate(reviews_count=Count("reviews"), reviews_avg=Avg("reviews__rating"))
    filterset_fields = ("category__id", "store__id")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProductGetSerializer

        elif self.action == "upload_images":
            return ProductCreateImageSerializer
        else:
            return ProductCreateSerializer

    @action(detail=True, methods=["post"],
            serializer_class=ProductCreateImageSerializer
            )
    def upload_images(self, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs["pk"])
        self.check_object_permissions(self.request, product)
        img_serializer = self.serializer_class(data=self.request.data)
        img_serializer.is_valid(raise_exception=True)
        product_images = map(lambda img: ProductImage(product=product, image=img),
                             img_serializer.validated_data["images"])
        ProductImage.objects.bulk_create(product_images)
        return Response(status=200)

    @action(methods=["delete"], detail=True, url_path="image/(?P<image_id>[^/]+)")
    def image(self, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs["pk"])
        self.check_object_permissions(self.request, product)
        product_image = get_object_or_404(ProductImage, id=kwargs["image_id"])
        product_image.image.delete()
        product_image.delete()
        return Response(status=204)


class ProductReviewDeleteView(GenericViewSet, DestroyModelMixin):
    queryset = ProductReview.objects.all()


class ProductReviewListCreateView(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return ProductReview.objects.select_related("owner") \
            .filter(product_id=self.kwargs.get("product_id"))

    def create(self, request, *args, **kwargs):
        review_serializer = self.serializer_class(data=request.data)
        review_serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, id=self.kwargs.get("product_id"))
        review = ProductReview.objects.create(**review_serializer.validated_data, product=product,
                                              owner=self.request.user)
        response_serializer = self.serializer_class(review)
        return Response(response_serializer.data, status=201)
