from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager

ROLE = (
    ("doctor", "Doctor"),
    ("patient", "patient"),
)


class User(AbstractUser):
    """
        Custom user model with extra fields
    """
    username = None
    role = models.CharField(choices=ROLE, max_length=20, default="patient", error_messages={"required": "Role must be provided"})
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = UserManager()


class Profile(models.Model):
    """
        User profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
