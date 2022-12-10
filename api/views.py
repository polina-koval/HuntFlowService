import datetime
import json

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (
    ApplicantSerializer,
    TagSerializer,
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
        app_hf_id = js["event"]["applicant"]["id"]
        app_phone = js["event"]["applicant"]["phone"]
        app_email = js["event"]["applicant"]["email"]
        app_first_name = js["event"]["applicant"]["first_name"]
        app_last_name = js["event"]["applicant"]["last_name"]
        app_middle_name = js["event"]["applicant"]["middle_name"]
        if js["event"]["applicant"]["birthday"] is not None:
            app_birth_date = datetime.datetime.strptime(
                js["event"]["applicant"]["birthday"], "%Y-%m-%d"
            )
        else:
            app_birth_date = None
        app_position = js["event"]["applicant"]["position"]
        app_defaults = {
            "phone": app_phone,
            "email": app_email,
            "position": app_position,
            "first_name": app_first_name,
            "middle_name": app_middle_name,
            "last_name": app_last_name,
            "birth_date": app_birth_date,
        }
        applicant, _ = Applicant.objects.update_or_create(
            hf_id=app_hf_id,
            defaults=app_defaults,
        )
        applicant.tags.clear()
        if js["changes"] and js["changes"]["applicant_tags"]:
            tags = js["event"]["applicant_tags"]
            for tag in tags:
                tag_obj, _ = Tag.objects.get_or_create(
                    name=tag["name"], hf_id=tag["id"]
                )
                applicant.tags.add(tag_obj)
        return Response({}, status=status.HTTP_200_OK)


class VacancyWebHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        body = request.body
        js = json.loads(body)
        vac_log = js["event"]["vacancy_log"]
        if vac_log["state"]:
            position = js["event"]["vacancy"]["position"]
            vac_hf_id = js["event"]["vacancy"]["id"]
            if vac_log["state"] == "OPEN":
                vacancy, _ = Vacancy.objects.get_or_create(
                    hf_id=vac_hf_id,
                    defaults={
                        "position": position,
                        "status": Vacancy.Statuses.OPEN,
                    },
                )
                applicants = search_applicants(position=position)
                add_applicant_to_vacancy(applicants, vac_hf_id)
            if vac_log["state"] == "REMOVED":
                Vacancy.objects.filter(position=position).delete()
        return Response({}, status=status.HTTP_200_OK)
