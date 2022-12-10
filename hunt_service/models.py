from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Applicant(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, related_name="applicants")


class Vacancy(models.Model):
    class Statuses(models.TextChoices):
        OPEN = "Open"
        CLOSE = "Close"
        HOLD = "Hold"
        RESUME = "Resume"

    position = models.CharField(max_length=255)
    status = models.CharField(
        choices=Statuses.choices, default=Statuses.CLOSE, max_length=6
    )
