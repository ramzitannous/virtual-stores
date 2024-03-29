import os
from django.db.models import QuerySet
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def ping(request):
    return Response("pong")


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def info(request):
    branch = os.environ.get("GIT_BRANCH", "ref/head/local")[11:]
    sha_commit = os.environ.get("SHA_COMMIT", "null commit")[:7]
    release_info = {
        "version": f"{branch}-{sha_commit}",
        "branch": branch,
        "sha_commit": sha_commit
    }
    return JsonResponse(release_info, status=200)


class OwnerViewMixin(GenericAPIView):

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.filter(owner=self.request.user)
        return queryset
