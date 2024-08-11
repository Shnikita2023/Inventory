from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.base.decorators import validate_pk
from api.v1.base.serializers import ErrorResponseSerializer
from api.v1.stocks.serializers import StockSerializer
from apps.base.exceptions import ApplicationException
from apps.inventory.services.stocks import BaseStockService, ORMStockService


class StocksViewSet(viewsets.ViewSet):
    serializer_class = StockSerializer
    stock_response = openapi.Response("Успешный ответ", serializer_class)
    error_response = openapi.Response("Ошибка", ErrorResponseSerializer)

    def __init__(self, service: BaseStockService | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service or ORMStockService()

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: serializer_class(many=True),
        },
        operation_description="Получение списка складов.",
    )
    def list(self, request: Request) -> Response:
        stocks_serializer = self.service.get_stock_list()
        return Response(stocks_serializer.data)

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={
            status.HTTP_201_CREATED: stock_response,
            status.HTTP_400_BAD_REQUEST: error_response,
        },
        operation_description="Создание нового склада.",
    )
    def create(self, request: Request) -> Response:
        try:
            stock_serializer = self.service.create_stock(request.data)
            return Response(stock_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"detail": ex.detail}, status=ex.status_code)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: stock_response,
            status.HTTP_404_NOT_FOUND: error_response,
        },
        operation_description="Получение информации о складе по ID.",
    )
    @validate_pk
    def retrieve(self, request: Request, pk: int) -> Response:
        try:
            stock_serializer = self.service.get_stock_by_id(pk)
            return Response(stock_serializer.data, status.HTTP_200_OK)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={
            status.HTTP_200_OK: stock_response,
            status.HTTP_400_BAD_REQUEST: error_response,
        },
        operation_description="Обновление информации о складе.",
    )
    @validate_pk
    def update(self, request: Request, pk: int) -> Response:
        try:
            stock_serializer = self.service.update_stock(pk, request.data)
            return Response(stock_serializer.data, status=status.HTTP_200_OK)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("No Content"),
            status.HTTP_404_NOT_FOUND: error_response,
        },
        operation_description="Удаление склада по ID.",
    )
    @validate_pk
    def destroy(self, request: Request, pk: int) -> Response:
        try:
            self.service.delete_stock(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)
