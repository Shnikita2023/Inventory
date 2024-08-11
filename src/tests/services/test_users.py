import pytest
from rest_framework.exceptions import ValidationError

from apps.users.exceptions import UserAlreadyExists
from apps.users.models import User
from apps.users.services import BaseUserService
from tests.test_data import user_data, invalid_user_data


def test_register_user(user_service):
    serializer = user_service.register_user(user_data)
    assert serializer.data["username"] == "test_user"
    assert User.objects.count() == 1
    assert User.objects.get(username="test_user").phone_number == "8905131313"


def test_register_user_invalid(user_service: BaseUserService):
    with pytest.raises(ValidationError) as exc:
        user_service.register_user(invalid_user_data)

    assert "username" in exc.value.detail
    assert "Это поле не может быть пустым." in exc.value.detail["username"]


def test_register_user_duplicate_username(user_service: BaseUserService, create_user: User):
    duplicate_user_data = {
        "username": create_user.username,
        "password": create_user.password,
    }
    with pytest.raises(UserAlreadyExists) as exc:
        user_service.register_user(duplicate_user_data)

    assert exc.value.status_code == 400
    assert exc.value.message == f"User {create_user.username} already exists"
