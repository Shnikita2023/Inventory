from abc import ABC, abstractmethod

from rest_framework.exceptions import ValidationError

from api.v1.stocks.serializers import StockSerializer
from apps.inventory.exceptions import NotFoundError
from apps.inventory.models import Stock


class BaseStockService(ABC):
    @abstractmethod
    def create_stock(self, stock_data: dict[str, str]) -> StockSerializer:
        pass

    @abstractmethod
    def get_stock_by_id(self, stock_id: int) -> StockSerializer:
        pass

    @abstractmethod
    def get_stock_list(self) -> StockSerializer:
        pass

    @abstractmethod
    def delete_stock(self, stock_id: int) -> None:
        pass

    @abstractmethod
    def update_stock(self, stock_id: int, stock_data: dict[str, str]) -> StockSerializer:
        pass


class ORMStockService(BaseStockService):
    def create_stock(self, stock_data: dict[str, str]) -> StockSerializer:
        serializer = StockSerializer(data=stock_data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()
        return serializer

    def get_stock_list(self) -> StockSerializer:
        stock_models = Stock.objects.all()
        return StockSerializer(stock_models, many=True)

    def get_stock_by_id(self, stock_id: int) -> StockSerializer:
        try:
            stock_model = Stock.objects.get(pk=stock_id)
            return StockSerializer(stock_model)

        except Stock.DoesNotExist:
            raise NotFoundError("Stock", stock_id)

    def delete_stock(self, stock_id: int) -> None:
        try:
            stock = Stock.objects.get(pk=stock_id)
            stock.delete()

        except Stock.DoesNotExist:
            raise NotFoundError("Stock", stock_id)

    def update_stock(self, stock_id: int, stock_data: dict[str, str]) -> StockSerializer:
        try:
            stock_model = Stock.objects.get(pk=stock_id)
            serializer = StockSerializer(instance=stock_model, data=stock_data)

            if not serializer.is_valid():
                raise ValidationError(serializer.errors)

            serializer.save()
            return serializer

        except Stock.DoesNotExist:
            raise NotFoundError("Stock", stock_id)
