import pytest
from rest_framework.exceptions import ValidationError

from apps.inventory.exceptions import NotFoundError
from apps.inventory.models import Category, Stock, Equipment
from apps.inventory.services.equipments import BaseEquipmentService
from apps.users.models import User
from tests.test_data import updated_equipments_data


def test_create_equipment(
    equipment_service: BaseEquipmentService,
    create_user: User,
    create_category: Category,
    create_stock: Stock
):
    data_equipment = {
        "title": "Test Equipment",
        "quantity": 10,
        "category": create_category.id,
        "stock": create_stock.id,
        "user": create_user.pk,
    }
    equipment = equipment_service.create_equipment(data_equipment)
    serializer_equipment = equipment.data
    assert serializer_equipment["title"] == "Test Equipment"
    assert serializer_equipment["quantity"] == 10


def test_create_equipment_invalid(
        equipment_service: BaseEquipmentService,
        create_user: User,
        create_category: Category,
        create_stock: Stock
):
    invalid_data_equipment = {
        "title": "",
        "quantity": 10,
        "category": create_category.id,
        "stock": create_stock.id,
        "user": create_user.pk,
    }
    with pytest.raises(ValidationError) as exc:
        equipment_service.create_equipment(invalid_data_equipment)

    assert "title" in exc.value.detail
    assert "Это поле не может быть пустым." in exc.value.detail["title"]


def test_get_equipment_list(equipment_service: BaseEquipmentService, create_equipment: Equipment):
    equipment_list = equipment_service.get_equipment_list()
    assert len(equipment_list.data) == 1
    assert equipment_list.data[0]["title"] == "Test Equipment"


def test_get_equipment_by_id(equipment_service: BaseEquipmentService, create_equipment: Equipment):
    retrieved_equipment = equipment_service.get_equipment_by_id(create_equipment.id)
    assert retrieved_equipment.data["title"] == "Test Equipment"


def test_get_equipment_by_id_not_found(equipment_service: BaseEquipmentService):
    with pytest.raises(NotFoundError):
        equipment_service.get_equipment_by_id(999)


def test_delete_equipment(equipment_service: BaseEquipmentService, create_equipment: Equipment):
    equipment_service.delete_equipment(create_equipment.id)
    with pytest.raises(NotFoundError):
        equipment_service.get_equipment_by_id(create_equipment.id)


def test_delete_equipment_not_found(equipment_service: BaseEquipmentService):
    with pytest.raises(NotFoundError):
        equipment_service.delete_equipment(999)


def test_update_equipment(equipment_service: BaseEquipmentService, create_equipment: Equipment):
    updated_data_equipment = {
        "title": "Updated Equipment",
        "quantity": 20,
        "category": create_equipment.category.id,
        "stock": create_equipment.stock.id,
        "user": create_equipment.user.id,
    }
    updated_equipment = equipment_service.update_equipment(create_equipment.id, updated_data_equipment)
    serializer_equipment = updated_equipment.data
    assert serializer_equipment["title"] == "Updated Equipment"
    assert serializer_equipment["quantity"] == 20


def test_update_equipment_not_found(equipment_service: BaseEquipmentService):
    with pytest.raises(NotFoundError):
        equipment_service.update_equipment(999, updated_equipments_data)
