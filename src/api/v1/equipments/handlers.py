from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from api.v1.base.decorators import validate_pk
from api.v1.base.serializers import ErrorResponseSerializer
from apps.base.exceptions import ApplicationException
from apps.inventory.services.equipments import BaseEquipmentService, ORMEquipmentService
from .serializers import EquipmentCreateSerializer, EquipmentReadSerializer


class EquipmentsViewSet(viewsets.ViewSet):
    create_serializer_class = EquipmentCreateSerializer
    read_serializer_class = EquipmentReadSerializer
    equipment_response = openapi.Response("Успешный ответ", read_serializer_class)
    error_response = openapi.Response("Ошибка", ErrorResponseSerializer)

    def __init__(self, service: BaseEquipmentService | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service or ORMEquipmentService()

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: read_serializer_class(many=True),
        },
        operation_description="Получение списка оборудования.",
    )
    def list(self, request: Request) -> Response:
        equipment_serializer = self.service.get_equipment_list()
        return Response(equipment_serializer.data)

    @swagger_auto_schema(
        request_body=create_serializer_class,
        responses={
            status.HTTP_201_CREATED: equipment_response,
            status.HTTP_400_BAD_REQUEST: error_response,
        },
        operation_description="Создание нового оборудования.",
    )
    def create(self, request: Request) -> Response:
        try:
            equipment_serializer = self.service.create_equipment(request.data)
            return Response(equipment_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"detail": ex.detail}, status=ex.status_code)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: equipment_response,
            status.HTTP_404_NOT_FOUND: error_response,
        },
        operation_description="Получение информации об оборудовании по ID.",
    )
    @validate_pk
    def retrieve(self, request: Request, pk: int) -> Response:
        try:
            equipment_serializer = self.service.get_equipment_by_id(pk)
            return Response(equipment_serializer.data, status.HTTP_200_OK)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)

    @swagger_auto_schema(
        request_body=create_serializer_class,
        responses={
            status.HTTP_200_OK: equipment_response,
            status.HTTP_400_BAD_REQUEST: error_response,
        },
        operation_description="Обновление информации об оборудовании.",
    )
    @validate_pk
    def update(self, request: Request, pk: int) -> Response:
        try:
            equipment_serializer = self.service.update_equipment(pk, request.data)
            return Response(equipment_serializer.data, status=status.HTTP_200_OK)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("No Content"),
            status.HTTP_404_NOT_FOUND: error_response,
        },
        operation_description="Удаление оборудования по ID.",
    )
    @validate_pk
    def destroy(self, request: Request, pk: int) -> Response:
        try:
            self.service.delete_equipment(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ApplicationException as ex:
            return Response({"detail": ex.message}, status=ex.status_code)
