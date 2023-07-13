from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Band(models.Model):
    class Genre(models.TextChoices):
        """sert pour la création d'un liste à dérouler ou l'on peut choisir uniquement un genre"""

        HIP_HOP = "HH"
        SYNTH_POP = "SP"
        ALTERNATIVE_ROCK = "AR"
        RAP = "RP"

    name = models.fields.CharField(max_length=100)
    genre = models.fields.CharField(choices=Genre.choices, max_length=5)
    biography = models.fields.CharField(max_length=1000)
    year_formed = models.fields.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2021)]
    )
    active = models.fields.BooleanField(default=True)
    official_homepage = models.fields.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    class Type(models.TextChoices):
        """sert pour la création d'un liste à dérouler ou l'on peut choisir uniquement un genre"""

        RECORDS = "RS"
        CLOTHINGS = "CS"
        POSTERS = "PS"
        MISCELLEANEOUS = "MS"

    title = models.fields.CharField(max_length=100)
    description = models.fields.CharField(max_length=1000)
    sold = models.fields.BooleanField(default=False)
    year_formed = models.fields.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2023)],
        null=True,
        blank=True,
    )

    type = models.fields.CharField(choices=Type.choices, max_length=5)
    band = models.ForeignKey(Band, null=True, on_delete=models.SET_NULL)



