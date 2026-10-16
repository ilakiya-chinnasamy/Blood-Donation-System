from django.db import models


class Donor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    email = models.EmailField(blank=True, default="")
    city = models.CharField(max_length=100, default="")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BloodRequest(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(
        max_length=3, choices=BLOOD_GROUPS
    )
    city = models.CharField(max_length=100)
    contact_email = models.EmailField()
    units = models.PositiveSmallIntegerField(default=1)
    hospital = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        default="Pending",
        choices=[
            ("Pending", "Pending"),
            ("Fulfilled", "Fulfilled"),
            ("Cancelled", "Cancelled"),
        ],
    )

    def __str__(self):
        return f"{self.blood_group} - {self.city}"


class DonorAlert(models.Model):
    donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE,
        related_name="blood_alerts",
    )
    blood_request = models.ForeignKey(
        BloodRequest,
        on_delete=models.CASCADE,
        related_name="alerts",
    )
    message = models.CharField(max_length=250)
    email_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Alert for {self.donor}"
height = models.FloatField(null=True, blank=True)
weight = models.FloatField(null=True, blank=True)
bmi = models.FloatField(null=True, blank=True)
state = models.CharField(max_length=100, blank=True, default="")