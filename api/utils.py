import json
import pprint

import requests
from django.conf import settings


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
        print(response.status_code)
        print(response.content)
