from rest_framework import serializers
from djoser.serializers import UserCreatePasswordRetypeSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from accounts.enums import AccountStatus, AccountTypes
from accounts.models import Account


class AccountGetSerializer(serializers.ModelSerializer):
    on_trial = serializers.BooleanField(read_only=True)
    status = serializers.ChoiceField(read_only=True, choices=[(s, s) for s in AccountStatus])
    type = serializers.ChoiceField(read_only=True, choices=[(s, s) for s in AccountTypes])
    email = serializers.EmailField(read_only=True)
    image = VersatileImageFieldSerializer(sizes="profile")

    class Meta:
        model = Account
        fields = ("id", "email", "image", "phone", "first_name",
                  "last_name", "type", "status", "on_trial", "create_date")


class AccountCreateSerializer(UserCreatePasswordRetypeSerializer):
    re_password = serializers.CharField(allow_blank=False, allow_null=False)

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = UserCreatePasswordRetypeSerializer.Meta.fields +\
                 ("re_password", "image", "phone", "first_name", "last_name", "type")
