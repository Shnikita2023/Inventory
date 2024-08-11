from django.db import models
from django.utils.text import slugify

from apps.users.models import User


class Stock(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="Название")
    location = models.CharField(max_length=255, verbose_name="Место хранения")

    class Meta:
        db_table: str = "stock"
        verbose_name: str = "Склад"
        verbose_name_plural: str = "Склады"

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        db_table: str = "category"
        verbose_name: str = "Категория"
        verbose_name_plural: str = "Категории"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Equipment(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="Название")
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="equipments")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="equipments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="equipments")

    class Meta:
        db_table: str = "equipment"
        verbose_name: str = "Оборудования"
        verbose_name_plural: str = "Оборудовании"

    def __str__(self):
        return self.title
