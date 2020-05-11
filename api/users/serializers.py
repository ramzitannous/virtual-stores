from rest_framework import serializers
from djoser.serializers import UserCreatePasswordRetypeSerializer
from users.models import CustomUser


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "image", "phone")


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    re_password = serializers.CharField(allow_blank=False, allow_null=False)

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = UserCreatePasswordRetypeSerializer.Meta.fields +\
                 ("re_password", "image", "phone")
