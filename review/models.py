from typing import Collection, Iterable, Optional
from unittest import TextTestRunner
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

FULL_STAR = "★"
EMPTY_STAR = "☆"


class Ticket(models.Model):
    """ticket model waiting for an user review"""

    title = models.CharField(
        max_length=128,
        verbose_name="Titre",
    )
    description = models.TextField(max_length=2048, blank=True, null=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(null=True)
    time_edited = models.DateTimeField(null=True)
    time_last_entry = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.title}"

    def resize_image(self):
        pass

    def save(self, *args, **kwargs):
        # modification time
        if self.time_created:
            self.time_edited = self.time_last_entry = timezone.now()

        # creation time
        if not self.time_created:
            self.time_created = self.time_last_entry = timezone.now()

        super().save(*args, **kwargs)


class Review(models.Model):
    """main review model"""

    rating = models.IntegerField(
        verbose_name="Note",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True,
    )
    star = models.CharField(null=True, max_length=5)
    headline = models.CharField(max_length=128, verbose_name="Intitulé", null=True)
    body = models.TextField(
        max_length=8192, verbose_name="Commentaire", blank=True, null=True
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    time_created = models.DateTimeField(null=True)
    time_edited = models.DateTimeField(null=True)
    time_last_entry = models.DateTimeField(auto_now_add=True, null=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True)
    self_review_instance = models.BooleanField(default=False)
    self_review = models.ForeignKey(to="self", on_delete=models.SET_NULL, null=True)

    def set_null(self, *args, **kwargs):
        """erase the tierce review"""

        self.user = None
        self.rating = None
        self.star = None
        self.headline = None
        self.body = None
        self.time_created = None
        self.time_edited = None
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.time_last_entry = timezone.now()
        # modification time
        if self.user and self.time_created:
            self.time_edited = timezone.now()

        # creation time
        if self.user and not self.time_created:
            self.time_created = timezone.now()

        # star field
        if self.user:
            self.star = self.rating * FULL_STAR + (5 - self.rating) * EMPTY_STAR

        super().save(*args, **kwargs)

    """Book/article review model"""


class Follower(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower"
    )
    followed_user = models.ForeignKey(
        verbose_name="Nom d'utilisateur",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed",
    )
    description = models.CharField(max_length=255, null=True)
    # Your UserFollows model definition goes here

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        )

    def save(self, *args, **kwargs):
        self.description = (
            f"{str(self.user).capitalize()} follows {str(self.followed_user).capitalize()}"
        )
        super().save(*args, **kwargs)
