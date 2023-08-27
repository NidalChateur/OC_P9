from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from PIL import Image

from authentication.models import User

FULL_STAR = "★"
EMPTY_STAR = "☆"


class Ticket(models.Model):
    """fields of the book or article."""

    WIDTH = User.WIDTH

    title = models.CharField(
        max_length=128,
        verbose_name="Titre",
    )
    author = models.CharField(
        max_length=128, verbose_name="Auteur", null=True, blank=True
    )
    product_type = models.CharField(
        max_length=128,
        choices=(
            ("Livre", "Livre"),
            ("Article", "Article"),
        ),
        verbose_name="Type",
        null=True,
        blank=True,
    )
    release_date = models.IntegerField(null=True, blank=True, verbose_name="Année")
    description = models.TextField(max_length=2048, blank=True, null=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(null=True)
    time_edited = models.DateTimeField(null=True, blank=True)
    time_last_entry = models.DateTimeField(null=True)
    slug_title = models.SlugField(max_length=128, null=True)
    slug_author = models.SlugField(max_length=128, null=True)

    def __str__(self):
        return f"{self.title}"

    def resize_image(self):
        """Resize the image while maintaining the original height/width aspect ratio
        width == 200px"""

        if self.image:
            image = Image.open(self.image)

            # get the original height/width aspect ratio
            width, height = image.size

            # get the new height/width aspect ratio
            new_width = self.WIDTH
            new_height = int(height * (new_width / width))

            # resize the image
            image = image.resize((new_width, new_height), Image.LANCZOS)

            # Save
            image.save(self.image.path)

    def save(self, *args, **kwargs):
        # modification time
        if self.time_created:
            self.time_edited = self.time_last_entry = timezone.now()

        # creation time
        if not self.time_created:
            self.time_created = self.time_last_entry = timezone.now()

        self.slug_title = slugify(self.title)

        if self.author:
            self.slug_author = slugify(self.author)

        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    """fields of the review.
    If the author of the ticket and the review are the same : it is a self_review !"""

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
    time_edited = models.DateTimeField(null=True, blank=True)
    time_last_entry = models.DateTimeField(auto_now_add=True, null=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True)
    is_self_review = models.BooleanField(default=False)
    self_review = models.ForeignKey(to="self", on_delete=models.SET_NULL, null=True)
    overall_rating = models.IntegerField(
        verbose_name="Note Total",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
    )

    def update_overall_rating(self):
        """used for ranking page :
        self.overall_rating = self.rating + self.self_review.rating"""

        self.overall_rating = 0
        if self.rating and self.self_review:
            self.overall_rating = self.rating + self.self_review.rating
        elif self.rating:
            self.overall_rating = self.rating
        elif self.self_review:
            self.overall_rating = self.self_review.rating

    def delete_self_review_rating(self, *args, **kwargs):
        """when the self_review is deleted, it updates self.overall_rating"""

        self.overall_rating = self.rating
        super().save(*args, **kwargs)

    def set_null(self, *args, **kwargs):
        """erase the tierce review"""

        self.user = None
        self.rating = None
        self.star = None
        self.headline = None
        self.body = None
        self.time_created = None
        self.time_edited = None
        self.update_overall_rating()
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

        # is_self_review
        if self.user == self.ticket.user:
            self.is_self_review = True

        self.update_overall_rating()
        super().save(*args, **kwargs)


class Relation(models.Model):
    """offer users the ability to follow or block other users"""

    # user_1 can follow or block user_2
    user_1 = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower"
    )
    # user_2 can followed or blocked by user_1
    user_2 = models.ForeignKey(
        verbose_name="Nom d'utilisateur",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed",
    )
    # type of the relation : 'follows' or 'blocks'
    type = models.CharField(
        max_length=128,
        null=True,
        choices=(
            ("blocks", "blocks"),
            ("follows", "follows"),
        ),
    )
    description = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = (
            "user_1",
            "user_2",
        )

    def save(self, *args, **kwargs):
        self.description = f"{str(self.user_1).capitalize()} {self.type} {str(self.user_2).capitalize()}"
        super().save(*args, **kwargs)
