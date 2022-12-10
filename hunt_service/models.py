from django.db import models


class Tag(models.Model):
    hf_id = models.PositiveIntegerField(
        unique=True, help_text="ID in the Huntflow service"
    )
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Applicant(models.Model):
    hf_id = models.PositiveIntegerField(
        unique=True, help_text="ID in the Huntflow service"
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255)
    tags = models.ManyToManyField(
        "Tag",
        related_name="applicants",
        blank=True,
    )

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class Vacancy(models.Model):
    class Statuses(models.TextChoices):
        OPEN = "Open"
        CLOSE = "Close"
        HOLD = "Hold"
        RESUME = "Resume"

    hf_id = models.PositiveIntegerField(
        unique=True, help_text="ID in the Huntflow service"
    )
    position = models.CharField(max_length=255)
    status = models.CharField(
        choices=Statuses.choices, default=Statuses.CLOSE, max_length=6
    )
    applicants = models.ManyToManyField("Applicant", related_name="vacancies")

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return self.position
