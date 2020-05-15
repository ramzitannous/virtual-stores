from django.db.models import QuerySet
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def ping(request):
    return Response("pong")


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
