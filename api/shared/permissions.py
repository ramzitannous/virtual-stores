from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from accounts.permissions import BusinessAccount
from shared.models import OwnerModel


class AppPermission(IsAuthenticatedOrReadOnly):
    """
        Admin: can do anything
        Owner Model: only his owner can change it and retrieve it
        else: check if it is read only
        some APIs need Business Account Permissions
    """

    def has_object_permission(self, request, view, obj: OwnerModel):
        if request.user.is_staff:
            return True

        if request.method not in SAFE_METHODS and isinstance(obj, OwnerModel)\
                and hasattr(obj, "owner"):
            return request.user == obj.owner

        return super().has_permission(request, view)


BUSINESS_PERMISSIONS = (AppPermission, BusinessAccount)
