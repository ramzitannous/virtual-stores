import logging

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def response_exception_handler(exception: Exception, context):
    response = exception_handler(exception, context)

    logger.exception(exception)

    if response is None:
        response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response.data = {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "exception": str(type(exception)),
            "details": [repr(exception)]
        }

    elif isinstance(exception, APIException):
        response.status_code = exception.status_code
        response.data = {
            "status_code": exception.status_code,
            "exception": str(type(exception)),
            "details": [exception.detail]
        }

    return response

logger = logging.getLogger("GlobalException")
