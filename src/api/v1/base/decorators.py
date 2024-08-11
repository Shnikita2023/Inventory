from collections.abc import Callable
from typing import Any

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


def validate_pk(func: Callable[..., Response]) -> Callable[..., Response]:
    def wrapper(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        if int(pk) <= 0:
            return Response({"detail": "ID must be greater than 0."}, status=status.HTTP_400_BAD_REQUEST)

        return func(self, request, pk, *args, **kwargs)

    return wrapper
