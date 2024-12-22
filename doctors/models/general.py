from datetime import timedelta
from django.db import models

from accounts.models import User


class TimeRange(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    is_active = models.BooleanField(default=True)
    slots_per_hour = models.PositiveIntegerField(default=4)

    def get_slot_duration(self):
        """Returns slot duration in minutes"""
        return 60 // self.slots_per_hour

    def get_available_slots(self, date):
        """
        Returns list of available time slots for given date
        Example: ['9:00', '9:15', '9:30', '9:45', '10:00', ...]
        """
        slot_duration = self.get_slot_duration()
        # Implementation to generate slots based on start, end, and duration
        slots = []
        current_time = self.start
        while current_time < self.end:
            slots.append(current_time.strftime("%H:%M"))
            current_time += timedelta(minutes=slot_duration)
        return slots

    class Meta:
        unique_together = ("start", "end")


class Saturday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_range = models.ManyToManyField(TimeRange)


class Sunday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_range = models.ManyToManyField(TimeRange)


class Monday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_range = models.ManyToManyField(TimeRange)


class Tuesday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_range = models.ManyToManyField(TimeRange)


class Wednesday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_range = models.ManyToManyField(TimeRange)


class Thursday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_range = models.ManyToManyField(TimeRange)


class Friday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_range = models.ManyToManyField(TimeRange)
