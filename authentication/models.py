from django.db import models
from django.contrib.auth.models import AbstractUser

from PIL import Image


class User(AbstractUser):
    """user model"""

    WIDTH = 200

    image = models.ImageField(
        verbose_name="Photo de profil", blank=True, null=True, default=None
    )

    def __str__(self):
        return f"{str(self.username).capitalize()}"

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
        """Override the save method with the resize_image"""

        super().save(*args, **kwargs)
        self.resize_image()
