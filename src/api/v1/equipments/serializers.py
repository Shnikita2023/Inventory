from rest_framework import serializers

from api.v1.categories.serializers import CategorySerializer
from api.v1.stocks.serializers import StockSerializer
from api.v1.users.serializers import RegisterUserSerializer
from apps.inventory.models import Equipment


class EquipmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("title", "quantity", "category", "stock", "user")


class EquipmentReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user = RegisterUserSerializer(read_only=True)
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = ("id", "title", "quantity", "category", "stock", "user")
