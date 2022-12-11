from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, RequestsClient

from api.tests.factories import ApplicantFactory, VacancyFactory
from hunt_service.models import Applicant, Tag, Vacancy


class ApplicantWebhookTest(APITestCase):
    def webhook_response(self):
        url = "http://testserver" + reverse("applicant_webhook")
        self.client = RequestsClient()
        response = self.client.post(
            url,
            json=self.order_data,
            headers={
                "Content-Type": "application/json",
                "X-Huntflow-Signature": "secret",
            },
        )
        return response

    @patch("api.utils.get_hmac", return_value="secret")
    def test_webhook_add_applicant(self, mock_get_hmac):
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

    @patch("api.utils.get_hmac", return_value="secret")
    def test_webhook_add_tag_to_applicant(self, mock_get_hmac):
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


class VacancyWebhookTest(APITestCase):
    def webhook_response(self):
        url = "http://testserver" + reverse("vacancy_webhook")
        self.client = RequestsClient()
        response = self.client.post(
            url,
            json=self.order_data,
            headers={
                "Content-Type": "application/json",
                "X-Huntflow-Signature": "secret",
            },
        )
        return response

    @patch("api.utils.get_hmac", return_value="secret")
    def test_webhook_open_vacancy(self, mock_get_hmac):
        self.order_data = {
            "changes": {},
            "event": {
                "vacancy": {
                    "account_division": None,
                    "account_region": None,
                    "applicants_to_hire": 1,
                    "body": None,
                    "company": None,
                    "conditions": None,
                    "created": "2022-12-11",
                    "deadline": None,
                    "fill_quotas": [
                        {
                            "applicants_to_hire": 1,
                            "closed": None,
                            "created": "2022-12-11T12:03:01+03:00",
                            "deadline": None,
                            "id": 62,
                            "vacancy_request": None,
                        }
                    ],
                    "frame_id": 62,
                    "hidden": False,
                    "id": 62,
                    "money": None,
                    "multiple": False,
                    "parent": None,
                    "position": "TeamLead",
                    "priority": 0,
                    "requirements": None,
                    "state": "OPEN",
                    "values": {},
                },
                "vacancy_log": {
                    "close_reason": None,
                    "created": "2022-12-11T12:03:01+03:00",
                    "hold_reason": None,
                    "id": 227,
                    "state": "OPEN",
                },
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
                "event_id": "295",
                "event_type": "VACANCY",
                "retry": 0,
                "version": "2.0",
                "webhook_action": "ADD",
            },
        }
        response = self.webhook_response()
        vacancy = Vacancy.objects.first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            vacancy.position,
            self.order_data["event"]["vacancy"]["position"],
        )