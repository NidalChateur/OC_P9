from unittest import TextTestRunner
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django import forms


class Ticket(models.Model):
    """ticket model waiting for an user review"""

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True, null=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, default=None)
    time_created = models.DateTimeField(null=True, default=None)
    time_edited = models.DateTimeField(null=True, default=None)
    time_last_entry = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """Book/article review model"""

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.IntegerField(
        verbose_name="Note",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        null=True,
        default=None,
    )
    star = models.CharField(null=True, default=None, max_length=5)
    headline = models.CharField(
        max_length=128, verbose_name="Intitulé", null=True, default=None
    )
    body = models.TextField(
        max_length=8192, verbose_name="Commentaire", blank=True, null=True, default=None
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None
    )
    time_created = models.DateTimeField(null=True, default=None)
    time_edited = models.DateTimeField(null=True, default=None)
    time_last_entry = models.DateTimeField(auto_now_add=True, null=True)

    """ second review is filled when the current user adds his own review
        to an existant review"""

    second_review = models.ForeignKey(
        to="self", on_delete=models.CASCADE, null=True, default=None
    )


""" class UserFollows(models.Model):
    # Your UserFollows model definition goes here

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        ) """
