from djoser.views import UserViewSet as DjoserUserViewSet


class AccountViewSet(DjoserUserViewSet):
    def get_queryset(self):
        queryset = super().queryset.select_related("address")
        return queryset
