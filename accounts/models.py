from urllib.parse import urljoin
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager
from utils.file_utils import profile_photo_directory_path

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

    objects = CustomUserManager()

    def __unicode__(self):
        return self.username


class Profile(models.Model):
    """
        User profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default="defaults/user.png", upload_to=profile_photo_directory_path)

    @property
    def image(self):
        return self.avatar.url if self.avatar.storage.exists(self.avatar.name) else "{}defaults/user.png".format(settings.MEDIA_URL)
