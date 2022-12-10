import datetime

import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from hunt_service.models import Applicant, Tag, Vacancy


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    hf_id = FuzzyInteger(low=1, high=99999)
    name = factory.Sequence(lambda n: f"Tag{n}")


class ApplicantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Applicant

    hf_id = FuzzyInteger(low=1, high=99999)
    first_name = factory.Sequence(lambda n: f"First_name{n}")
    last_name = factory.Sequence(lambda n: f"Last_name{n}")
    middle_name = factory.Sequence(lambda n: f"Middle_name{n}")
    birth_date = datetime.date(year=1998, month=9, day=12)
    phone = factory.Sequence(lambda n: f"+798012345{n}")
    email = factory.Sequence(lambda n: f"email{n}@test.com")
    position = factory.Sequence(lambda n: f"Position{n}")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.tags.add(*extracted)


class VacancyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vacancy

    hf_id = FuzzyInteger(low=1, high=99999)
    status = FuzzyChoice(Vacancy.Statuses.choices)
    position = factory.Sequence(lambda n: f"Position{n}")

    @factory.post_generation
    def applicants(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.applicants.add(*extracted)
