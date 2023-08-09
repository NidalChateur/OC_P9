from django import forms
from django.contrib.auth import get_user_model

from review.models import Ticket, Review, Follower
from review.validators import validate_followed_user
from authentication.models import User
from django.core.exceptions import ValidationError


class TicketForm(forms.ModelForm):
    """ticket form"""

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    """review form"""

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

    rating = forms.IntegerField(
        widget=forms.RadioSelect(
            choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
        ),
        label="Note",
    )


class FollowerForm(forms.Form):
    create = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    followed_user = forms.CharField(
        max_length=128, label="Nom d'utilisateur", validators=[validate_followed_user]
    )

class DeleteFollowerForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)