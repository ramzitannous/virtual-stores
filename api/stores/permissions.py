from django.core.handlers.wsgi import WSGIRequest
from rest_framework.permissions import BasePermission, SAFE_METHODS

from stores.models import Store


class StorePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request: WSGIRequest, view, obj: Store):
        if obj.owner == request.user:
            return True
        return False
