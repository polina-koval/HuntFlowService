from django.contrib import admin

from hunt_service.models import Applicant, Tag, Vacancy


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    pass


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass
