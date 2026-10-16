from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST

from .models import Donor, BloodRequest, DonorAlert

def home(request):
    context = {
        "total_donors": Donor.objects.count(),
        "total_requests": BloodRequest.objects.count(),
        "pending_requests": BloodRequest.objects.filter(status="Pending").count(),
        "recent_requests": BloodRequest.objects.order_by("-created_at")[:5],
    }
    return render(request, "donors/home.html", context)

def register_donor(request):
    if request.method == "POST":
        Donor.objects.create(
            name=request.POST.get("name", "").strip(),
            age=request.POST.get("age"),
            gender=request.POST.get("gender", "").strip(),
            blood_group=request.POST.get("blood_group", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            address=request.POST.get("address", "").strip(),
            email=request.POST.get("email", "").strip(),
            city=request.POST.get("city", "").strip(),
        )
        messages.success(request, "Donor registered successfully!")
        return redirect("home")

    return render(request, "donors/register.html")

def donor_list(request):
    return render(request, "donors/donor_list.html", {
        "donors": Donor.objects.all(),
    })

def request_blood(request):
    if request.method != "POST":
        return render(request, "donors/request_blood.html")

    patient_name = request.POST.get("patient_name", "").strip()
    blood_group = request.POST.get("blood_group", "").strip()
    city = request.POST.get("city", "").strip()
    contact_email = request.POST.get("contact_email", "").strip()
    hospital = request.POST.get("hospital", "").strip()

    try:
        units = int(request.POST.get("units", "1"))
    except (ValueError, TypeError):
        units = 0

    if (
        not patient_name
        or not city
        or not contact_email
        or blood_group not in dict(BloodRequest.BLOOD_GROUPS)
        or not 1 <= units <= 10
    ):
        messages.error(request, "Please enter valid request details.")
        return redirect("request_blood")

    blood_request = BloodRequest.objects.create(
        patient_name=patient_name,
        blood_group=blood_group,
        city=city,
        contact_email=contact_email,
        units=units,
        hospital=hospital,
    )

    donors = Donor.objects.filter(
        blood_group__iexact=blood_group,
        city__iexact=city,
        is_available=True,
    )

    matching_count = donors.count()
    emails_sent = 0
    emails_failed = 0
    donors_without_email = 0

    for donor in donors:
        alert = DonorAlert.objects.create(
            donor=donor,
            blood_request=blood_request,
            message=(
                f"LifeLink blood request: {blood_group} blood needed in "
                f"{city}. Please check your availability."
            ),
        )

        if not donor.email:
            donors_without_email += 1
            print(f"Donor {donor.name} has no email address.")
            continue

        subject = f"LifeLink - {blood_group} Blood Needed in {city}"

        message = f"""Dear {donor.name},

Greetings from LifeLink!

A blood request matching your blood group has been registered in our system. Your willingness to help could make a real difference to someone in need.

BLOOD REQUEST DETAILS

Blood Group: {blood_group}
City: {city}
Patient / Reference: {patient_name}
Hospital: {hospital or 'Not specified'}
Units Required: {units}

HOW YOU CAN HELP

If you are available and medically eligible to donate, please contact the requester using the contact details provided on LifeLink.

Please verify the request and coordinate with the hospital before making arrangements. Donation is voluntary and should only take place when you are medically eligible.

Thank you for being part of our lifesaving community.

With gratitude,
Team LifeLink
Every Drop Saves a Life!
"""

        try:
            result = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL or None,
                recipient_list=[donor.email],
                fail_silently=False,
            )

            if result == 1:
                alert.email_sent = True
                alert.save(update_fields=["email_sent"])
                emails_sent += 1
                print(f"Email sent successfully to {donor.email}")
            else:
                emails_failed += 1
                print(f"Email was not confirmed for {donor.email}")

        except Exception as e:
            emails_failed += 1
            print(
                f"Email failed for {donor.email}: "
                f"{type(e).__name__}: {e}"
            )

    messages.success(
        request,
        f"Blood request saved. {matching_count} matching donor(s) found, "
        f"{emails_sent} email(s) sent, {emails_failed} email(s) failed, "
        f"and {donors_without_email} donor(s) had no email address."
    )

    return redirect("alerts")

def alerts(request):
    all_alerts = DonorAlert.objects.select_related(
        "donor", "blood_request"
    ).order_by("-created_at")

    context = {
        "alerts": all_alerts,
        "alert_count": all_alerts.count(),
        "email_count": all_alerts.filter(email_sent=True).count(),
        "unread_count": all_alerts.filter(is_read=False).count(),
    }

    return render(request, "donors/alerts.html", context)

@require_POST
def mark_alert_read(request, alert_id):
    alert = DonorAlert.objects.filter(id=alert_id).first()

    if alert is None:
        messages.error(request, "Alert not found.")
        return redirect("alerts")

    alert.is_read = True
    alert.save(update_fields=["is_read"])

    messages.success(request, "Alert marked as read.")
    return redirect("alerts")