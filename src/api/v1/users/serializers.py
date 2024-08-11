import re
from typing import Final

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(min_length=5)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "address",
            "phone_number",
        )

    def validate_password(self, password: str) -> str:
        password_regex: Final[str] = r"[!@#$%^&*()\-_=+{};:,<.>|\[\]\\/?]"
        # Проверка на длину пароля
        if len(password) < 8 or len(password) > 50:
            raise ValidationError("Пароль должен содержать от 8 до 50 символов.")

        # Проверка на наличие хотя бы одной заглавной буквы
        if not any(c.isupper() for c in password):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")

        # Проверка на наличие хотя бы одной строчной буквы
        if not any(c.islower() for c in password):
            raise ValidationError("Пароль должен содержать хотя бы одну строчную букву")

        # Проверка на наличие хотя бы одной цифры
        if not any(c.isdigit() for c in password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру")

        # Проверка на наличие хотя бы одного специального символа
        if not re.search(password_regex, password):
            raise ValidationError("Пароль должен содержать хотя бы одну специальную символ")

        return password

    def create(self, validated_data) -> User:
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
