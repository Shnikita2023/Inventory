from typing import Literal

from django.contrib import admin

from apps.inventory.models import Category, Equipment, Stock


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields: dict[str, tuple[Literal["title"]]] = {"slug": ("title",)}
    list_display = ("id", "title", "slug", "description")
    list_filter = ("title",)
    search_fields = ("title", "description")


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "quantity", "category", "stock", "user")
    list_filter = ("title",)
    search_fields = ("title", "description")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "location")
    list_filter = ("title", "location")
    search_fields = ("title", "location")
