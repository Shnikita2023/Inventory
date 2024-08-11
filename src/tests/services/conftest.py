import pytest

from apps.inventory.models import Category, Stock, Equipment
from apps.inventory.services.categories import ORMCategoryService
from apps.inventory.services.equipments import ORMEquipmentService
from apps.inventory.services.stocks import ORMStockService
from apps.users.models import User
from apps.users.services import UserService


@pytest.fixture
def category_service(db) -> ORMCategoryService:
    return ORMCategoryService()


@pytest.fixture
def equipment_service(db) -> ORMEquipmentService:
    return ORMEquipmentService()


@pytest.fixture
def stock_service(db) -> ORMStockService:
    return ORMStockService()


@pytest.fixture
def user_service(db) -> UserService:
    return UserService()


@pytest.fixture
def create_category() -> Category:
    return Category.objects.create(
        title="Test Category",
        description="This is a test category.",
    )


@pytest.fixture
def create_stock() -> Stock:
    return Stock.objects.create(
        title="Test Stock",
        location="Moscow",
    )


@pytest.fixture
def create_user() -> User:
    return User.objects.create(
        username="test_user",
        password="Test!fa23",
    )


@pytest.fixture
def create_equipment(create_category: Category, create_stock: Stock, create_user: User) -> Equipment:
    return Equipment.objects.create(
        title="Test Equipment", quantity=10, category=create_category, stock=create_stock, user=create_user
    )
