from django.contrib import admin

from hunt_service.models import Applicant, Tag, Vacancy


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "hf_id"]


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "position", "hf_id"]


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ["position", "hf_id", "status"]
