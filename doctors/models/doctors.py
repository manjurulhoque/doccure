from django.db import models

from accounts.models import User


class Education(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="educations"
    )
    college = models.CharField(max_length=300)
    degree = models.CharField(max_length=100)
    year_of_completion = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Doctor Educations"

    def __str__(self) -> str:
        return (
            f"{self.user.get_full_name()} -> {self.college} -> {self.degree}"
        )


class Experience(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="experiences"
    )
    institution = models.CharField(max_length=300)
    from_year = models.IntegerField(null=True, blank=True)
    to_year = models.IntegerField(null=True, blank=True)
    working_here = models.BooleanField("Currently working here", default=False)
    designation = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Work & Experience"
        verbose_name_plural = "Works & Experiences"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} -> {self.institution}"


class Review(models.Model):
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="doctor_reviews"
    )
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="patient_reviews"
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["doctor", "patient"]
        ordering = ["-created_at"]


class Specialty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    doctors = models.ManyToManyField(User, related_name="specialties")
