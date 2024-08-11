from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.base.exceptions import ApplicationException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ApplicationException):
        response = Response({"error": exc.message}, status=exc.status_code)

    return response
