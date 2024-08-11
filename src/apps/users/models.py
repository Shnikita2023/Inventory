from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name="Номер телефона")
    address = models.TextField(max_length=250, blank=True, null=True, verbose_name="Адрес")

    class Meta:
        db_table: str = "user"
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"

    def __str__(self):
        return self.username
