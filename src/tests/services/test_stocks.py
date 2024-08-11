import pytest
from rest_framework.exceptions import ValidationError

from apps.inventory.exceptions import NotFoundError
from apps.inventory.models import Stock
from apps.inventory.services.stocks import BaseStockService
from tests.test_data import stock_data, invalid_stock_data, updated_stock_data


def test_create_stock(stock_service: BaseStockService):
    stock = stock_service.create_stock(stock_data)
    serializer_stock = stock.data
    assert serializer_stock["title"] == "New Stock"
    assert serializer_stock["location"] == "Saint Petersburg"


def test_create_stock_invalid(stock_service: BaseStockService):
    with pytest.raises(ValidationError):
        stock_service.create_stock(invalid_stock_data)


def test_get_stock_list(stock_service: BaseStockService, create_stock: Stock):
    stock_list = stock_service.get_stock_list()
    assert len(stock_list.data) == 1
    assert stock_list.data[0]["title"] == "Test Stock"


def test_get_stock_by_id(stock_service: BaseStockService, create_stock: Stock):
    retrieved_stock = stock_service.get_stock_by_id(create_stock.id)
    assert retrieved_stock.data["title"] == "Test Stock"


def test_get_stock_by_id_not_found(stock_service):
    with pytest.raises(NotFoundError):
        stock_service.get_stock_by_id(999)


def test_delete_stock(stock_service: BaseStockService, create_stock: Stock):
    stock_service.delete_stock(create_stock.id)
    with pytest.raises(NotFoundError):
        stock_service.get_stock_by_id(create_stock.id)


def test_delete_stock_not_found(stock_service):
    with pytest.raises(NotFoundError):
        stock_service.delete_stock(999)


def test_update_stock(stock_service: BaseStockService, create_stock: Stock):
    updated_stock = stock_service.update_stock(create_stock.id, updated_stock_data)
    serializer_stock = updated_stock.data
    assert serializer_stock["title"] == "Updated Stock"
    assert serializer_stock["location"] == "Updated Location"


def test_update_stock_not_found(stock_service):
    with pytest.raises(NotFoundError):
        stock_service.update_stock(999, updated_stock_data)
