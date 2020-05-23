from rest_framework import serializers
from djoser.serializers import UserCreatePasswordRetypeSerializer
from shared.serializers import Base64ThumbnailSerializer
from accounts.enums import AccountStatus, AccountTypes
from accounts.models import Account, AccountAddress


class AccountAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountAddress
        fields = '__all__'


class AccountGetSerializer(serializers.ModelSerializer):
    on_trial = serializers.BooleanField(read_only=True)
    status = serializers.ChoiceField(read_only=True, choices=[(s, s) for s in AccountStatus])
    type = serializers.ChoiceField(read_only=True, choices=[(s, s) for s in AccountTypes])
    email = serializers.EmailField(read_only=True)
    image = Base64ThumbnailSerializer(sizes="profile")
    address = AccountAddressSerializer(many=False)

    class Meta:
        model = Account
        fields = ("id", "email", "image", "phone", "first_name",
                  "last_name", "type", "status", "on_trial", "create_date",
                  "address", "gender")

    def update(self, instance, validated_data):
        if "address" in validated_data:
            new_address = validated_data.pop("address")
            if instance.address is None:
                instance.address = AccountAddress()

            for k, v in new_address.items():
                setattr(instance.address, k, v)
                instance.address.save()
        return super().update(instance, validated_data)


class AccountCreateSerializer(UserCreatePasswordRetypeSerializer):
    re_password = serializers.CharField(allow_blank=False, allow_null=False)
    image = Base64ThumbnailSerializer(sizes="profile")
    address = AccountAddressSerializer(many=False, required=False)

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = UserCreatePasswordRetypeSerializer.Meta.fields +\
                 ("re_password", "image", "phone", "first_name",
                  "last_name", "type", "gender", "address")

    def validate(self, attrs):
        address = attrs.pop("address")
        attrs = super().validate(attrs)
        attrs["address"] = address
        return attrs

    def create(self, validated_data):
        if "address" in validated_data and validated_data["address"] is not None:
            address_data = validated_data.pop("address")
            address_serializer = AccountAddressSerializer(data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address = AccountAddress.objects.create(**address_serializer.validated_data)
            account = Account.objects.create(**validated_data, address=address)
            return account
        return Account.objects.create(**validated_data)
