from rest_framework import serializers

from apps.inventory.models import Category


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "title", "description", "slug")
