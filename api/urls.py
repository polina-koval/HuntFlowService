from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import ApplicantViewSet, TagViewSet, VacancyViewSet
from api.webhooks import ApplicantWebHook, VacancyWebHook

schema_view = get_schema_view(
    openapi.Info(
        title="Huntflow integration service",
        default_version="v1.1.0",
        description="Test task from Huntflow",
        contact=openapi.Contact(email="koval6polina@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
router = routers.DefaultRouter()
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"applicants", ApplicantViewSet, basename="applicant")
router.register(r"vacancies", VacancyViewSet, basename="vacancy")
urlpatterns = router.urls
urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        "applicant_webhook/",
        ApplicantWebHook.as_view(),
        name="applicant_webhook",
    ),
    path("vacancy_webhook/", VacancyWebHook.as_view(), name="vacancy_webhook"),
]
