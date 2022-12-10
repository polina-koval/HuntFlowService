from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, RequestsClient

from api.tests.factories import ApplicantFactory, VacancyFactory
from hunt_service.models import Applicant, Tag


class ApplicantWebhookTest(APITestCase):
    def webhook_response(self):
        url = "http://testserver" + reverse("applicant_webhook")
        self.client = RequestsClient()
        response = self.client.post(
            url,
            json=self.order_data,
            headers={
                "Content-Type": "application/json"
                #     "X_Wc_Webhook_Signature": "secret",
            },
        )
        return response

    def test_webhook_add_applicant(self):
        self.order_data = {
            "changes": {},
            "event": {
                "applicant": {
                    "birthday": None,
                    "company": None,
                    "email": None,
                    "externals": [
                        {
                            "account_source": None,
                            "auth_type": "NATIVE",
                            "id": 78,
                            "updated": "2022-12-10 " "20:08:24",
                        }
                    ],
                    "first_name": "Иван",
                    "id": 78,
                    "last_name": "Иванов",
                    "middle_name": "Иванович",
                    "money": None,
                    "pd_agreement": None,
                    "phone": None,
                    "photo": None,
                    "position": "Role3",
                    "questionary": None,
                    "skype": None,
                    "social": [],
                    "values": {},
                },
                "applicant_log": {
                    "calendar_event": None,
                    "comment": None,
                    "created": "2022-12-10T20:08:24+03:00",
                    "employment_date": None,
                    "files": [],
                    "hired_in_fill_quota": None,
                    "id": 206,
                    "rejection_reason": None,
                    "removed": None,
                    "source": None,
                    "status": None,
                    "survey_answer_of_type_a": None,
                    "type": "ADD",
                    "vacancy": None,
                },
                "applicant_tags": [],
            },
            "meta": {
                "account": {
                    "id": 14,
                    "name": "test-ff499c5dfa9d4a0e952eae470",
                    "nick": "test-ff499c5dfa9d4a0e952eae470",
                },
                "author": {
                    "email": "author@gmail.com",
                    "id": 13,
                    "meta": None,
                    "name": "author@gmail.com",
                },
                "domain": "dev-100.huntflow.dev",
                "event_id": "276",
                "event_type": "APPLICANT",
                "retry": 0,
                "version": "2.0",
                "webhook_action": "ADD",
            },
        }
        response = self.webhook_response()
        applicant = Applicant.objects.first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            applicant.first_name,
            self.order_data["event"]["applicant"]["first_name"],
        )

    def test_webhook_add_tag_to_applicant(self):
        applicant = ApplicantFactory()
        self.order_data = {
            "changes": {"applicant_tags": {"from": []}},
            "event": {
                "applicant": {
                    "birthday": applicant.birth_date.strftime("%Y-%m-%d"),
                    "company": None,
                    "email": applicant.email,
                    "externals": [
                        {
                            "account_source": None,
                            "auth_type": "NATIVE",
                            "id": applicant.hf_id,
                            "updated": "2022-12-10 " "20:08:24",
                        }
                    ],
                    "first_name": applicant.first_name,
                    "id": applicant.hf_id,
                    "last_name": applicant.last_name,
                    "middle_name": applicant.middle_name,
                    "money": None,
                    "pd_agreement": None,
                    "phone": applicant.phone,
                    "photo": None,
                    "position": applicant.position,
                    "questionary": None,
                    "skype": None,
                    "social": [],
                    "values": {},
                },
                "applicant_log": {
                    "calendar_event": None,
                    "comment": None,
                    "created": "2022-12-10T20:20:43+03:00",
                    "employment_date": None,
                    "files": [],
                    "hired_in_fill_quota": None,
                    "id": 207,
                    "rejection_reason": None,
                    "removed": None,
                    "source": None,
                    "status": None,
                    "survey_answer_of_type_a": None,
                    "type": "EDIT",
                    "vacancy": None,
                },
                "applicant_tags": [
                    {"color": "e37b00", "id": 29, "name": "Резерв"}
                ],
            },
            "meta": {
                "account": {
                    "id": 14,
                    "name": "test-ff499c5dfa9d4a0e952eae470",
                    "nick": "test-ff499c5dfa9d4a0e952eae470",
                },
                "author": {
                    "email": "test@gmail.com",
                    "id": 13,
                    "meta": None,
                    "name": "test@gmail.com",
                },
                "domain": "dev-100.huntflow.dev",
                "event_id": "277",
                "event_type": "APPLICANT",
                "retry": 0,
                "version": "2.0",
                "webhook_action": "EDIT",
            },
        }
        response = self.webhook_response()
        tag = Tag.objects.first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            tag.name, self.order_data["event"]["applicant_tags"][0]["name"]
        )
        self.assertEqual(tag.applicants.first(), applicant)
