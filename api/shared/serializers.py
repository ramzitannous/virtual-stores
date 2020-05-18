from rest_framework import serializers

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