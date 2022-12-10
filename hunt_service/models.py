from django.db import models


class Tag(models.Model):
    hf_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Applicant(models.Model):
    hf_id = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    tags = models.ManyToManyField(
        "Tag",
        related_name="applicants",
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"


class Vacancy(models.Model):
    class Statuses(models.TextChoices):
        OPEN = "Open"
        CLOSE = "Close"
        HOLD = "Hold"
        RESUME = "Resume"
    hf_id = models.PositiveIntegerField(unique=True)
    position = models.CharField(max_length=255)
    status = models.CharField(
        choices=Statuses.choices, default=Statuses.CLOSE, max_length=6
    )
    applicants = models.ManyToManyField("Applicant", related_name="vacancies")

    def __str__(self):
        return self.position
