from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.parsers import MultiPartParser
from djangorestframework_camel_case.parser import CamelCaseJSONParser


class AccountViewSet(DjoserUserViewSet):
    def get_parsers(self):
        method = self.request.method.lower()
        action = self.action_map.get(method)
        if action in ["create", "update", "partial_update"]:
            return [MultiPartParser()]
        elif action == "me" and method in ["patch", "put"]:
            return [MultiPartParser()]
        return [CamelCaseJSONParser()]
