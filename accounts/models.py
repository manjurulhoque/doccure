from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (
    ("doctor", "Doctor"),
    ("patient", "patient"),
)


class User(AbstractUser):
    """
        Custom user model with extra fields
    """
    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(choices=ROLE, max_length=20, default="patient", error_messages={"required": "Role must be provided"})
    email = models.EmailField(
        blank=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.username


class Profile(models.Model):
    """
        User profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
