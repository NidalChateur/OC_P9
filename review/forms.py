from django import forms

from review.models import Ticket, Review


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


class RelationForm(forms.Form):
    followed_user = forms.CharField(
        max_length=128,
        label="Nom d'utilisateur",
    )
