from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from review.models import Follower


def validate_followed_user(value):
    """used to validate FollowerForm"""

    User = get_user_model()
    try:
        user = User.objects.get(username=value)
    except User.DoesNotExist:
        raise ValidationError("Cet utilisateur n'existe pas.")

