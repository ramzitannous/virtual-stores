from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, SAFE_METHODS
from .enums import AccountTypes, AccountStatus


class VerifiedAccountOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.user.status == AccountStatus.VERIFIED


class BusinessAccount(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.method == "POST" and not request.user.type == AccountTypes.BUSINESS:
            return False

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.method in SAFE_METHODS:
            return True

        return bool(request.user.type == AccountTypes.BUSINESS and \
                    request.user.status == AccountStatus.VERIFIED)


class NormalAccount(IsAuthenticated):
    pass


class TrialAccount(BusinessAccount):
    def has_object_permission(self, request, view, obj):
        return bool(
            super().has_object_permission(request, view, obj)
            and request.user.on_trial
        )
