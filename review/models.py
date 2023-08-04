from typing import Collection, Iterable, Optional
from unittest import TextTestRunner
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    time_last_entry = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.title}"
    
    def resize_image(self):
        pass

    def save(self, *args, **kwargs):
        # modification time
        if self.user and self.time_created:
            self.time_edited = timezone.now()

        # creation time
        if self.user and not self.time_created:
            self.time_created = timezone.now()

        super().save(*args, **kwargs)


class SelfReview(models.Model):
    """self review"""

    rating = models.IntegerField(
        verbose_name="Note",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
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

    def save(self, *args, **kwargs):
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


class Review(models.Model):
    """main review model"""

    rating = models.IntegerField(
        verbose_name="Note",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
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
    self_review = models.ForeignKey(to=SelfReview, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
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


""" class UserFollows(models.Model):
    # Your UserFollows model definition goes here

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        ) """
