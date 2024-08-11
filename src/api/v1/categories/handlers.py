from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from apps.base.exceptions import ApplicationException
from apps.inventory.services.categories import BaseCategoryService, ORMCategoryService

from ..base.decorators import validate_pk
from ..base.serializers import ErrorResponseSerializer
from .serializers import CategorySerializer


class CategoriesViewSet(viewsets.ViewSet):
    serializer_class = CategorySerializer
    category_response = openapi.Response("Успешный ответ", serializer_class)
    error_response = openapi.Response("Ошибка", ErrorResponseSerializer)

    def __init__(self, service: BaseCategoryService | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service or ORMCategoryService()

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: serializer_class(many=True),
        },
        operation_description="Получение списка категорий.",
    )
    def list(self, request: Request) -> Response:
        categories_serializer = self.service.get_category_list()
        return Response(categories_serializer.data)

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={
            status.HTTP_201_CREATED: category_response,
            status.HTTP_400_BAD_REQUEST: error_response,
        },
        operation_description="Создание новой категории.",
    )
    def create(self, request: Request) -> Response:
        try:
            category_serializer = self.service.create_category(request.data)
            return Response(category_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"detail": ex.detail}, status=ex.status_code)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: category_response,
            status.HTTP_400_BAD_REQUEST: error_response,
        },
        operation_description="Получение информации о категории по ID.",
    )
    @validate_pk
    def retrieve(self, request: Request, pk: int) -> Response:
        try:
            category_serializer = self.service.get_category_by_id(pk)
            return Response(category_serializer.data, status.HTTP_200_OK)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={
            status.HTTP_200_OK: category_response,
            status.HTTP_400_BAD_REQUEST: error_response,
        },
        operation_description="Обновление информации о категории.",
    )
    @validate_pk
    def update(self, request, pk: int) -> Response:
        try:
            category_serializer = self.service.update_category(pk, request.data)
            return Response(category_serializer.data, status=status.HTTP_200_OK)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("No Content"),
            status.HTTP_400_BAD_REQUEST: error_response,
        },
        operation_description="Удаление категории по ID.",
    )
    @validate_pk
    def destroy(self, request: Request, pk: int) -> Response:
        try:
            self.service.delete_category(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)
