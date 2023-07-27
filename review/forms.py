from django import forms

from review.models import Ticket, Review


class TicketForm(forms.ModelForm):
    """ticket form"""

    class Meta:
        model = Ticket
        fields = "__all__"

class ReviewForm(forms.ModelForm):
    """review form"""

    class Meta:
        model = Review
        fields = "__all__"
