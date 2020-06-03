from djoser.views import UserViewSet as DjoserUserViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from social_core.exceptions import SocialAuthBaseException
from requests import HTTPError
from accounts.serializers import JWTResponseSerializer, SocialInputSerializer


class AccountViewSet(DjoserUserViewSet):
    def get_queryset(self):
        queryset = super().queryset.select_related("address")
        return queryset


class SocialLoginView(GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = SocialInputSerializer
    response_serializer = JWTResponseSerializer

    @swagger_auto_schema(operation_description="Social login",
                         request_body=SocialInputSerializer,
                         responses={
                             "200": JWTResponseSerializer,
                             "401": "unauthorized"
                         })
    def post(self, *args, **kwargs):
        token_serializer = self.get_serializer_class()(data=self.request.data,
                                                       context={"request": self.request})
        token_serializer.is_valid(raise_exception=True)
        try:
            user = token_serializer.do_login()
        except (SocialAuthBaseException, HTTPError) as e:
            raise NotAuthenticated(e)
        if user is None:
            raise NotAuthenticated("Invalid Social Token")

        serializer_class = self.response_serializer
        if not hasattr(serializer_class, "get_token"):
            raise TypeError("serializer class must implement get_token method")

        token = serializer_class.get_token(user)
        token_response = {
            "refresh": str(token),
            "access": str(token.access_token)
        }
        response_serializer = serializer_class(data=token_response)
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.validated_data)
