import json

import requests
from django.conf import settings
from rest_framework import status

from hunt_service.models import Applicant, Vacancy


def search_applicants(position):
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


def add_applicant_to_vacancy(applicant_data, vacancy_id):
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
            print(vac_obj)
            app_obj = Applicant.objects.filter(hf_id=int(app_id)).first()
            print(app_obj)
            vac_obj.applicants.add(app_obj)
            vac_obj.save()
