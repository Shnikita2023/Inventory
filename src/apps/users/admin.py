from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "is_staff", "is_active", "is_superuser")
    list_filter = ("username", "is_staff", "is_active", "is_superuser")
    search_fields = ("username",)
    exclude = ("password",)
