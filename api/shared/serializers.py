from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from drf_base64.fields import Base64FieldMixin
from accounts.models import Account
from shared.models import BaseReview


class ReviewOwnerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ("id", "full_name", "image")


class ReviewSerializer(serializers.ModelSerializer):
    owner = ReviewOwnerSerializer(read_only=True)

    class Meta:
        model = BaseReview
        fields = ("id", "title", "rating", "create_date", "owner")


class Base64ThumbnailSerializer(Base64FieldMixin, VersatileImageFieldSerializer):
    def to_internal_value(self, data):
        return super().to_internal_value(data)
