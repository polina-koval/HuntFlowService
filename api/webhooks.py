import json

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import (
    add_applicant_to_vacancy,
    create_or_update_applicant,
    search_applicants,
)
from hunt_service.models import Tag, Vacancy


class ApplicantWebHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        body = request.body
        js = json.loads(body)
        applicant = create_or_update_applicant(js["event"]["applicant"])
        applicant.tags.clear()
        if js["changes"] and js["changes"].get("applicant_tags", None):
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
        json_data = json.loads(request.body)
        vac_log = json_data["event"]["vacancy_log"]
        if vac_log["state"]:
            position = json_data["event"]["vacancy"]["position"]
            vac_hf_id = json_data["event"]["vacancy"]["id"]
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
