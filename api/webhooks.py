import hashlib
import hmac
import json

from django.conf import settings
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


def get_hmac(secret_key, request_body):
    """
    Returns X-Huntflow-Signature
    """
    signature = hmac.new(
        secret_key.encode("utf-8"), request_body, hashlib.sha256
    ).hexdigest()
    return signature


def hmac_is_valid(secret_key, request_body, received_hmac):
    """
    Check the received X-Huntflow-Signature with the expected
    Returns: bool
    """
    expected_hmac = get_hmac(secret_key, request_body)
    return expected_hmac == received_hmac


class ApplicantWebHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        body = request.body
        # ------------------
        request_hmac = request.headers.get("X-Huntflow-Signature")
        print(settings.APPLICANT_WEBHOOK_SECRET)
        if request_hmac and hmac_is_valid(
            settings.APPLICANT_WEBHOOK_SECRET,
            request.body,
            request_hmac,
        ):
            print("Yeeeep")
        else:
            print("NOOOOOO")
        # ------------------
        js = json.loads(body)
        if js.get("event"):
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
