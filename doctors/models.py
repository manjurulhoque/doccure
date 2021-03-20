from django.db import models

from accounts.models import User


class TimeRange(models.Model):
    start = models.TimeField()
    end = models.TimeField()


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
