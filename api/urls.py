from django.urls import path
from rest_framework import routers

from api.views import VacancyWebHook, UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
urlpatterns = router.urls
urlpatterns += [
    path("vac/", VacancyWebHook.as_view()),
]
