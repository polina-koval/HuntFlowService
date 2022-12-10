from rest_framework import viewsets

from api.serializers import (
    ApplicantSerializer,
    TagSerializer,
    VacancySerializer,
)
from hunt_service.models import Applicant, Tag, Vacancy


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ApplicantViewSet(viewsets.ModelViewSet):

    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer


class VacancyViewSet(viewsets.ModelViewSet):

    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
