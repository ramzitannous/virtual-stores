from rest_framework import serializers

from shared.serializers import ReviewSerializer
from stores.models import Store, StoreAddress, StoreReview


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
    address = StoreAddressSerializer(required=True)

    class Meta:
        model = Store
        fields = "__all__"

    def create(self, validated_data):
        address = StoreAddress.objects.create(**validated_data.pop("address"))
        return Store.objects.create(**validated_data, address=address)

    def update(self, instance: Store, validated_data: dict):
        if "address" in validated_data:
            new_address = validated_data["address"]
            for k, v in new_address.items():
                setattr(instance.address, k, v)
            instance.address.save(force_update=True, update_fields=new_address.keys())
            return instance
        else:
            return super().update(instance, validated_data)


class StoreReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        model = StoreReview
