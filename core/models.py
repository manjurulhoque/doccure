from django.db import models


class Speciality(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="specialities/", null=True, blank=True)

    def __str__(self):
        return self.name
