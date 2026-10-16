from django.contrib import admin
from .models import Donor, BloodRequest, DonorAlert


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "age",
        "blood_group",
        "phone",
        "email",
        "city",
        "is_available",
    )
    search_fields = ("name", "email", "city", "blood_group")


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "blood_group",
        "city",
        "hospital",
        "units",
        "status",
        "created_at",
    )
    list_filter = ("blood_group", "city", "status")
    search_fields = ("patient_name", "city", "contact_email")


@admin.register(DonorAlert)
class DonorAlertAdmin(admin.ModelAdmin):
    list_display = (
        "donor",
        "blood_request",
        "email_sent",
        "is_read",
        "created_at",
    )
    list_filter = ("email_sent", "is_read")