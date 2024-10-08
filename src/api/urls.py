from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Inventory API",
        default_version="v1",
        description="Учёт оборудование на складах",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nikita@mail.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("docs<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("v1/", include("api.v1.urls")),
]
