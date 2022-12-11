import datetime
import hashlib
import hmac
import json

import requests
from django.conf import settings
from rest_framework import status

from hunt_service.models import Applicant, Tag, Vacancy


def create_or_update_applicant(app_data):
    """
    Create or update applicant from the webhook data
    Returns Tag object
    """
    app_hf_id = app_data.get("id")
    app_phone = app_data.get("phone")
    app_email = app_data.get("email")
    app_first_name = app_data.get("first_name")
    app_last_name = app_data.get("last_name")
    app_middle_name = app_data.get("middle_name")
    app_birth_date = app_data.get("birthday")
    if app_birth_date:
        app_birth_date = datetime.datetime.strptime(
            app_data["birthday"], "%Y-%m-%d"
        )
    app_position = app_data.get("position")
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
    return applicant


def get_or_create_tag(tag_data):
    """
    Get or create tag object from the webhook data
    Returns Tag object
    """
    tag_obj, _ = Tag.objects.get_or_create(
        name=tag_data["name"], hf_id=tag_data["id"]
    )
    return tag_obj


def search_applicants(position):
    """
    Search applicants by position field in the Huntflow service
    Returns array of applicants
    """
    params = {"q": position, "field": "position"}
    response = requests.get(
        f"https://dev-100-api.huntflow.dev/v2/accounts/"
        f"{settings.ORG_ID}/applicants/search",
        headers={
            "Authorization": f"Bearer {settings.API_KEY_HF}",
        },
        params=params,
    )
    data = json.loads(response.content.decode())
    return data


def add_applicant_to_vacancy(position, vacancy_id):
    """
    Assigns the first received applicant to a vacancy
    in the Huntflow service and its own service.
    """
    applicant_data = search_applicants(position=position)
    if (
        applicant_data
        and applicant_data["items"]
        and applicant_data["items"][0]
    ):
        app_data = applicant_data["items"][0]
        app_id = app_data["id"]
        params = {
            "vacancy": vacancy_id,
            "status": settings.VACANCY_DEFAULT_STATUS,
        }
        response = requests.post(
            f"https://dev-100-api.huntflow.dev/v2/accounts/"
            f"{settings.ORG_ID}/applicants/{app_id}/vacancy",
            headers={
                "Authorization": f"Bearer {settings.API_KEY_HF}",
            },
            json=params,
        )
        if response.status_code == status.HTTP_200_OK:
            vac_obj = Vacancy.objects.filter(hf_id=vacancy_id).first()
            app_obj = create_or_update_applicant(app_data)
            vac_obj.applicants.add(app_obj)
            vac_obj.save()


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
