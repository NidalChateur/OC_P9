from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def validate_followed_user(value):
    """used to validate FollowerForm : test if the followed_user field is an 
    existant user"""

    User = get_user_model()
    try:
        user = User.objects.get(username=value)
    except User.DoesNotExist:
        raise ValidationError("Cet utilisateur n'existe pas.")
