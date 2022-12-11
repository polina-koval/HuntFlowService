import json

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import (
    add_applicant_to_vacancy,
    create_or_update_applicant,
    get_or_create_tag,
    hmac_is_valid,
)
from hunt_service.models import Vacancy


class ApplicantWebHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle applicant webhook from Huntflow
        """
        request_hmac = request.headers.get("X-Huntflow-Signature")
        if request_hmac and hmac_is_valid(
            settings.APPLICANT_WEBHOOK_SECRET,
            request.body,
            request_hmac,
        ):
            json_data = json.loads(request.body)
            if "event" in json_data:
                event = json_data["event"]
                applicant = create_or_update_applicant(event["applicant"])
                applicant.tags.clear()
                if "applicant_tags" in event:
                    tags = event["applicant_tags"]
                    for tag in tags:
                        tag_obj = get_or_create_tag(tag)
                        if tag_obj:
                            applicant.tags.add(tag_obj)
                if "applicant_log" in event:
                    tag_data = event["applicant_log"].get("status")
                    if (
                        tag_data and tag_data["name"] == "Оффер принят"
                    ):  # TODO remove hardcode
                        tag_obj = get_or_create_tag(
                            change_in_hw=True, app_id=applicant.hf_id
                        )
                        if tag_obj:
                            applicant.tags.add(tag_obj)
                return Response({}, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VacancyWebHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle vacancy webhook from Huntflow
        """
        json_data = json.loads(request.body)
        request_hmac = request.headers.get("X-Huntflow-Signature")
        if request_hmac and hmac_is_valid(
                settings.VACANCY_WEBHOOK_SECRET,
                request.body,
                request_hmac,
        ):
            if "event" in json_data:
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
                        add_applicant_to_vacancy(position, vac_hf_id)
                        return Response({}, status=status.HTTP_200_OK)
                    elif vac_log["state"] == "REMOVED":
                        Vacancy.objects.filter(position=position).delete()
                        return Response({}, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
