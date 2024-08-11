from rest_framework import serializers

from apps.inventory.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("id", "title", "location")
