from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешает доступ на чтение всем аутентифицированным пользователям,
    а на запись только администраторам.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in ["GET"]:
            return True

        return request.user and request.user.is_superuser
