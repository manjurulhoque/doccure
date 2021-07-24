from django.db import models

from accounts.models import User


class Booking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
