from django.db import models
from accounts.models import User


class Booking(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="patient_bookings"
    )
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="doctor_bookings"
    )
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
            ("no_show", "No Show"),
        ],
        default="pending",
    )
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-booking_date", "-booking_time"]
        indexes = [
            models.Index(fields=["booking_date", "booking_time"]),
            models.Index(fields=["status"]),
        ]
