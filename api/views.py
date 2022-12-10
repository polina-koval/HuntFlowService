import datetime
import json
import pprint

import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (
    ApplicantSerializer,
    TagSerializer,
    UserSerializer,
    VacancySerializer,
)
from api.utils import add_applicant_to_vacancy, search_applicants
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


class ApplicantWebHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        body = request.body
        js = json.loads(body)
        app_phone = js["event"]["applicant"]["phone"]
        app_email = js["event"]["applicant"]["email"]
        app_first_name = js["event"]["applicant"]["first_name"]
        app_last_name = js["event"]["applicant"]["last_name"]
        app_middle_name = js["event"]["applicant"]["middle_name"]
        app_birth_date = datetime.datetime.strptime(
            js["event"]["applicant"]["birthday"], "%Y-%m-%d"
        )
        app_position = js["event"]["applicant"]["position"]
        app_defaults = {
            "phone": app_phone,
            "email": app_email,
            "position": app_position,
        }
        applicant, _ = Applicant.objects.update_or_create(
            first_name=app_first_name,
            middle_name=app_middle_name,
            last_name=app_last_name,
            birth_date=app_birth_date,
            defaults=app_defaults,
        )
        applicant.tags.clear()
        # pp = pprint.PrettyPrinter(indent=2, width=30, compact=True)
        # pp.pprint(js)
        if js["changes"] and js["changes"]["applicant_tags"]:
            tags = js["event"]["applicant_tags"]
            for tag in tags:
                tag_obj, _ = Tag.objects.get_or_create(name=tag["name"])
                applicant.tags.add(tag_obj)
        return Response({}, status=status.HTTP_200_OK)


class VacancyWebHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        body = request.body
        js = json.loads(body)
        # pp = pprint.PrettyPrinter(indent=2, width=30, compact=True)
        # pp.pprint(js)
        vac_log = js["event"]["vacancy_log"]
        if vac_log["state"]:
            position = js["event"]["vacancy"]["position"]
            if vac_log["state"] == "OPEN":
                vacancy, _ = Vacancy.objects.get_or_create(
                    position=position, defaults={"status": Vacancy.Statuses.OPEN}
                )
                vacancy_id = js["event"]["vacancy"]["id"]
                applicants = search_applicants(position=position)
                add_applicant_to_vacancy(applicants, vacancy_id)
            if vac_log["state"] == "REMOVED":
                Vacancy.objects.filter(position=position).delete()
        return Response({}, status=status.HTTP_200_OK)
