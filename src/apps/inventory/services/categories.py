from abc import ABC, abstractmethod

from rest_framework.exceptions import ValidationError

from api.v1.categories.serializers import CategorySerializer
from apps.inventory.exceptions import NotFoundError
from apps.inventory.models import Category


class BaseCategoryService(ABC):
    @abstractmethod
    def create_category(self, category_data: dict[str, str]) -> CategorySerializer:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> CategorySerializer:
        pass

    @abstractmethod
    def get_category_list(self) -> CategorySerializer:
        pass

    @abstractmethod
    def delete_category(self, category_id: int) -> None:
        pass

    @abstractmethod
    def update_category(self, category_id: int, category_data: dict[str, str]) -> CategorySerializer:
        pass


class ORMCategoryService(BaseCategoryService):
    def create_category(self, category_data: dict[str, str]) -> CategorySerializer:
        serializer = CategorySerializer(data=category_data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()
        return serializer

    def get_category_list(self) -> CategorySerializer:
        category_models = Category.objects.all()
        return CategorySerializer(category_models, many=True)

    def get_category_by_id(self, category_id: int):
        try:
            category_model = Category.objects.get(pk=category_id)
            return CategorySerializer(category_model)

        except Category.DoesNotExist:
            raise NotFoundError("Category", category_id)

    def delete_category(self, category_id: int) -> None:
        try:
            category = Category.objects.get(pk=category_id)
            category.delete()

        except Category.DoesNotExist:
            raise NotFoundError("Category", category_id)

    def update_category(self, category_id: int, category_data: dict[str, str]) -> CategorySerializer:
        try:
            category_model = Category.objects.get(pk=category_id)
            serializer = CategorySerializer(instance=category_model, data=category_data)

            if not serializer.is_valid():
                raise ValidationError(serializer.errors)

            serializer.save()
            return serializer

        except Category.DoesNotExist:
            raise NotFoundError("Category", category_id)
