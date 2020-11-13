from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from versatileimagefield.serializers import VersatileImageFieldSerializer
from products.enum import ProductSize
from products.models import Category, Product, ProductReview
from shared.serializers import ReviewSerializer, Base64ThumbnailSerializer
from stores.models import Store
from django.utils.translation import gettext_lazy as _


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("image_ppoi", "create_date", "last_updated")


class ProductGetImageSerializer(serializers.Serializer):
    image = VersatileImageFieldSerializer(read_only=False, sizes="product")
    id = serializers.UUIDField(read_only=True)


class ProductCreateImageSerializer(serializers.Serializer):
    images = serializers.ListSerializer(child=Base64ThumbnailSerializer(sizes="product", required=True))


class StoreSummary(serializers.ModelSerializer):
    address = None
    ppoi_field = None

    class Meta:
        model = Store
        fields = ("name", "id")


class ProductGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    colors = serializers.ListField(serializers.CharField(), default=list)
    sizes = serializers.ListField(serializers.ChoiceField(choices=[(s, s) for s in ProductSize], required=False),
                                  default=list)
    integer_sizes = serializers.ListField(
        serializers.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(45)]),
        default=list)
    images = ProductGetImageSerializer(many=True, read_only=True)
    extras = serializers.JSONField(default=dict, allow_null=False)

    reviews_count = serializers.IntegerField(read_only=True)
    reviews_avg = serializers.DecimalField(read_only=True, max_digits=4, decimal_places=2)

    store = StoreSummary(read_only=True)

    class Meta:
        model = Product
        exclude = ("owner",)


class ProductCreateSerializer(ProductGetSerializer):
    category = None
    store = None

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    store_id = serializers.UUIDField(required=True, write_only=True, allow_null=False)
    category_id = serializers.UUIDField(required=True, allow_null=False, write_only=True)

    class Meta:
        model = Product
        exclude = ("category", "store")

    def create(self, validated_data: dict):
        store_id = validated_data.pop("store_id")
        category_id = validated_data.pop("category_id")
        category = get_object_or_404(Category, id=category_id)
        store = get_object_or_404(Store, id=store_id)
        product = Product.objects.create(category=category, store=store, **validated_data)
        return product

    def update(self, instance, validated_data):
        if "store_id" in validated_data:  # prevent changing store
            raise ValidationError(_("can't change store"))
        if "category_id" in validated_data:
            category_id = validated_data.pop("category_id")
            category = get_object_or_404(Category, id=category_id)
            instance.category = category
        return super().update(instance, validated_data)


class ProductReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        model = ProductReview
