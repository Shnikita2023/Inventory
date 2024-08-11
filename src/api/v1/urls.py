from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.categories.handlers import CategoriesViewSet
from api.v1.equipments.handlers import EquipmentsViewSet
from api.v1.stocks.handlers import StocksViewSet
from api.v1.users.handlers import LoginView, RegisterView

router = DefaultRouter()

router.register(r"categories", CategoriesViewSet, basename="categories")
router.register(r"equipments", EquipmentsViewSet, basename="equipments")
router.register(r"stocks", StocksViewSet, basename="stocks")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/sign-up/", RegisterView.as_view(), name="register_user"),
    path("auth/login/", LoginView.as_view(), name="login_user"),
]
