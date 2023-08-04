from django import forms

from review.models import Ticket, Review, SelfReview


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
            choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
        ),
    )

    def __init__(self, *args, **kwargs):
        """change the label name"""

        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["rating"].label = "Note"


class SelfReviewForm(forms.ModelForm):
    """review form"""

    class Meta:
        model = SelfReview
        fields = ["headline", "rating", "body"]

    rating = forms.IntegerField(
        widget=forms.RadioSelect(
            choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
        ),
    )
