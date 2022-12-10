from django.db import models


class Tag(models.Model):
    name = models.CharField()


class Applicant(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    middle_name = models.CharField()
    phone = models.CharField()
    position = models.CharField()
    tags = models.ManyToManyField(Tag, related_name="applicants")


class Vacancy(models.Model):
    class Statuses(models.TextChoices):
        OPEN = "Open"
        CLOSE = "Close"
        HOLD = "Hold"
        RESUME = "Resume"

    position = models.CharField()
    status = models.CharField(choices=Statuses.choices, default=Statuses.CLOSE)
