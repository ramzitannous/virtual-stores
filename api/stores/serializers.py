from django.shortcuts import get_object_or_404
from rest_framework import serializers
from products.models import Category
from products.serializers import CategorySerializer
from shared.serializers import ReviewSerializer, Base64ThumbnailSerializer
from stores.models import Store, StoreReview, StoreAddress


class StoreAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAddress
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_active = serializers.BooleanField(read_only=True)
    owner_id = serializers.UUIDField(source="owner.id", read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    reviews_avg = serializers.DecimalField(read_only=True, max_digits=4, decimal_places=2)
    address = StoreAddressSerializer(required=True, many=False)
    image = Base64ThumbnailSerializer(sizes="store", required=False)
    deactivate_date = serializers.DateField(read_only=True)
    category_id = serializers.UUIDField(required=True, write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Store
        exclude = ("image_ppoi",)

    def create(self, validated_data):
        address = validated_data.pop("address")
        address_serializer = StoreAddressSerializer(data=address)
        address_serializer.is_valid(raise_exception=True)
        address = address_serializer.save()
        category = get_object_or_404(Category, id=validated_data.pop("category_id"))
        return Store.objects.create(**validated_data, address=address, category=category)

    def update(self, instance: Store, validated_data: dict):
        if "address" in validated_data:
            new_address = validated_data.pop("address")
            for k, v in new_address.items():
                setattr(instance.address, k, v)
                instance.address.save()
        return super().update(instance, validated_data)


class StoreReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        model = StoreReview
