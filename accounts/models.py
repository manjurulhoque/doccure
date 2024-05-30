from urllib.parse import urljoin
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from accounts.managers import CustomUserManager
from utils.file_utils import profile_photo_directory_path

ROLE = (
    ("doctor", "Doctor"),
    ("patient", "Patient"),
)


class User(AbstractUser):
    """
    Custom user model with extra fields
    """

    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(
        choices=ROLE,
        max_length=20,
        default="patient",
        error_messages={"required": "Role must be provided"},
    )
    email = models.EmailField(
        blank=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    registration_number = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip() or self.username

    def get_doctor_profile(self):
        """
        Return doctor profile URL
        """
        return reverse(
            "doctors:doctor-profile", kwargs={"username": self.username}
        )


class Profile(models.Model):
    """
    User profile
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    avatar = models.ImageField(
        default="defaults/user.png", upload_to=profile_photo_directory_path
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Profile of {}".format(self.user.username)

    @property
    def image(self):
        return (
            self.avatar.url
            if self.avatar.storage.exists(self.avatar.name)
            else "{}defaults/user.png".format(settings.MEDIA_URL)
        )
