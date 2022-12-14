from django.contrib.auth.models import User
from rest_framework import serializers

from hunt_service.models import Applicant, Tag, Vacancy


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "hf_id", "name"]


class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Applicant
        fields = [
            "id",
            "hf_id",
            "first_name",
            "last_name",
            "middle_name",
            "birth_date",
            "phone",
            "email",
            "position",
            "tags"
        ]


class VacancySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vacancy
        fields = [
            "id",
            "hf_id",
            "position",
            "status",
            "applicants",
        ]
