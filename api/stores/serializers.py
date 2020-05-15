from rest_framework import serializers
from drf_nested_serializer.serializers import NestedModelSerializer
from stores.models import Store, StoreReview
from accounts.models import Account


class StoreSerializer(NestedModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_active = serializers.BooleanField(read_only=True)
    owner_id = serializers.UUIDField(source="owner.id", read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    reviews_avg = serializers.DecimalField(read_only=True, max_digits=4, decimal_places=2)

    class Meta:
        model = Store
        fields = "__all__"
        nested_fields = ("address",)

    def update(self, instance: Store, validated_data: dict):
        if "address" in validated_data: 
            new_address = validated_data["address"]
            for k, v in new_address.items():
                setattr(instance.address, k, v)
            instance.address.save(force_update=True, update_fields=new_address.keys())
            return instance
        else:
            return super().update(instance, validated_data)


class StoreReviewOwnerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ("id", "full_name", "image")


class StoreReviewSerializer(serializers.ModelSerializer):
    owner = StoreReviewOwnerSerializer(read_only=True)

    class Meta:
        model = StoreReview
        fields = ("id", "title", "rating", "create_date", "owner")
