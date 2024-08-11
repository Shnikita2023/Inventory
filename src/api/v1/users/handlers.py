from typing import Any

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.base.serializers import ErrorResponseSerializer
from api.v1.users.serializers import RegisterUserSerializer
from apps.base.exceptions import ApplicationException
from apps.users.services import BaseUserService, UserService


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    equipment_response = openapi.Response("Успешный ответ", serializer_class)
    error_response = openapi.Response("Ошибка", ErrorResponseSerializer)

    def __init__(self, service: BaseUserService | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service or UserService()

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={
            status.HTTP_201_CREATED: equipment_response,
            status.HTTP_400_BAD_REQUEST: error_response,
        },
        operation_description="Регистрация пользователя.",
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            serializer = self.service.register_user(request.data)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except ValidationError as ex:
            return Response({"detail": ex.detail}, status=status.HTTP_400_BAD_REQUEST)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    token_response = openapi.Response("Успешный ответ", TokenObtainPairSerializer)
    error_response = openapi.Response("Ошибка", ErrorResponseSerializer)

    @swagger_auto_schema(
        request_body=TokenObtainPairSerializer,
        responses={
            status.HTTP_200_OK: token_response,
            status.HTTP_401_UNAUTHORIZED: error_response,
        },
        operation_description="Аутентификация пользователя и получение токена.",
    )
    def post(self, request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
