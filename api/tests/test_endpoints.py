from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.tests.factories import TagFactory, ApplicantFactory, VacancyFactory


class TagsEndpointTest(APITestCase):
    def setUp(self):
        self.api_client = APIClient()

    def test_tags_list(self):
        TagFactory.create_batch(5)
        response = self.api_client.get(reverse("tags-list"))
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_applicant_list(self):
        ApplicantFactory.create_batch(5)
        response = self.api_client.get(reverse("applicants-list"))
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vacancies_list(self):
        VacancyFactory.create_batch(5)
        response = self.api_client.get(reverse("vacancies-list"))
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)