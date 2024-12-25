from django.db import models


class Speciality(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="specialities/")

    def __str__(self):
        return self.name
