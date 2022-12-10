from django.urls import path
from rest_framework import routers

from api.views import ApplicantWebHook, UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
urlpatterns = router.urls
urlpatterns += [
    path("applicant_webhook/", ApplicantWebHook.as_view()),
]
