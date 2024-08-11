import pytest
from rest_framework.exceptions import ValidationError

from apps.inventory.exceptions import NotFoundError
from apps.inventory.models import Category
from apps.inventory.services.categories import BaseCategoryService
from tests.test_data import category_data, updated_category_data


def test_create_category(category_service: BaseCategoryService):
    serializer = category_service.create_category(category_data)
    assert serializer.data["title"] == "New Category"
    assert Category.objects.count() == 1


def test_create_category_invalid(category_service: BaseCategoryService):
    category_invalid_data = {
        "title": "",
        "description": "This is a new category.",
    }
    with pytest.raises(ValidationError) as exc:
        category_service.create_category(category_invalid_data)

    assert "title" in exc.value.detail
    assert "Это поле не может быть пустым." in exc.value.detail["title"]


def test_get_category_list(category_service: BaseCategoryService, create_category: Category):
    categories = category_service.get_category_list()
    assert len(categories.data) == 1
    assert categories.data[0]["title"] == "Test Category"


def test_get_category_by_id(category_service: BaseCategoryService, create_category: Category):
    category = category_service.get_category_by_id(create_category.id)
    assert category.data["title"] == "Test Category"


def test_get_category_by_id_not_found(category_service: BaseCategoryService):
    with pytest.raises(NotFoundError):
        category_service.get_category_by_id(999)


def test_update_category(category_service: BaseCategoryService, create_category: Category):
    serializer = category_service.update_category(create_category.id, updated_category_data)
    assert serializer.data["title"] == "New Category"
    assert serializer.data["description"] == "This is a new category."


def test_delete_category(category_service: BaseCategoryService, create_category: Category):
    category_service.delete_category(create_category.id)
    assert Category.objects.count() == 0


def test_delete_category_not_found(category_service: BaseCategoryService):
    with pytest.raises(NotFoundError):
        category_service.delete_category(999)
