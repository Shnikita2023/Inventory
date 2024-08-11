from abc import ABC, abstractmethod
from typing import Any

from rest_framework.exceptions import ValidationError

from api.v1.equipments.serializers import EquipmentCreateSerializer, EquipmentReadSerializer
from apps.inventory.exceptions import NotFoundError
from apps.inventory.models import Equipment


class BaseEquipmentService(ABC):
    @abstractmethod
    def create_equipment(self, equipment_data: dict[str, Any]) -> EquipmentReadSerializer:
        pass

    @abstractmethod
    def get_equipment_by_id(self, equipment_id: int) -> EquipmentReadSerializer:
        pass

    @abstractmethod
    def get_equipment_list(self) -> EquipmentReadSerializer:
        pass

    @abstractmethod
    def delete_equipment(self, equipment_id: int) -> None:
        pass

    @abstractmethod
    def update_equipment(self, equipment_id: int, equipment_data: dict[str, Any]) -> EquipmentReadSerializer:
        pass


class ORMEquipmentService(BaseEquipmentService):
    def create_equipment(self, equipment_data: dict[str, Any]) -> EquipmentReadSerializer:
        serializer = EquipmentCreateSerializer(data=equipment_data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()
        return EquipmentReadSerializer(serializer.instance)

    def get_equipment_list(self) -> EquipmentReadSerializer:
        equipment_models = Equipment.objects.select_related("category", "stock", "user").all()
        return EquipmentReadSerializer(equipment_models, many=True)

    def get_equipment_by_id(self, equipment_id: int) -> EquipmentReadSerializer:
        try:
            equipment_model = Equipment.objects.select_related("category", "stock", "user").get(pk=equipment_id)
            return EquipmentReadSerializer(equipment_model)

        except Equipment.DoesNotExist:
            raise NotFoundError("Equipment", equipment_id)

    def delete_equipment(self, equipment_id: int) -> None:
        try:
            equipment = Equipment.objects.get(pk=equipment_id)
            equipment.delete()

        except Equipment.DoesNotExist:
            raise NotFoundError("Equipment", equipment_id)

    def update_equipment(self, equipment_id: int, equipment_data: dict[str, Any]) -> EquipmentReadSerializer:
        try:
            equipment_model = Equipment.objects.get(pk=equipment_id)
            serializer = EquipmentCreateSerializer(instance=equipment_model, data=equipment_data)

            if not serializer.is_valid():
                raise ValidationError(serializer.errors)

            serializer.save()
            return EquipmentReadSerializer(serializer.instance)

        except Equipment.DoesNotExist:
            raise NotFoundError("Equipment", equipment_id)
