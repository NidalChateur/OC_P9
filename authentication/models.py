from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """user model"""

    profil_photo = models.ImageField(
        verbose_name="Photo de profil", blank=True, null=True, default=None
    )
