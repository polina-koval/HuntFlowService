from django.urls import path
from rest_framework import routers

from api.views import (
    ApplicantViewSet,
    ApplicantWebHook,
    TagViewSet,
    VacancyViewSet,
    VacancyWebHook,
)

router = routers.DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"applicants", ApplicantViewSet)
router.register(r"vacancies", VacancyViewSet)
urlpatterns = router.urls
urlpatterns += [
    path("applicant_webhook/", ApplicantWebHook.as_view()),
    path("vacancy_webhook/", VacancyWebHook.as_view()),
]
