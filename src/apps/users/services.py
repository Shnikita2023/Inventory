from abc import ABC, abstractmethod
from typing import Any

from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from api.v1.users.serializers import RegisterUserSerializer
from apps.users.exceptions import UserAlreadyExists


class BaseUserService(ABC):
    @abstractmethod
    def register_user(self, user_data: dict[str, Any]) -> RegisterUserSerializer:
        pass


class UserService(BaseUserService):
    def register_user(self, user_data: dict[str, Any]) -> RegisterUserSerializer:
        serializer = RegisterUserSerializer(data=user_data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        try:
            serializer.save()
            return serializer

        except IntegrityError:
            raise UserAlreadyExists(user_data["username"])
