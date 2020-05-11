from rest_framework.permissions import IsAuthenticated

from shared.models import OwnerModel


class OwnerPermissionOrAdmin(IsAuthenticated):

    def has_object_permission(self, request, view, obj: OwnerModel):
        if request.user.is_staff:
            return True
        return request.user == obj.owner
