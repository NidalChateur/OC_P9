from django import forms

from review.models import Ticket, Review


class TicketForm(forms.ModelForm):
    """ticket form"""

    class Meta:
        model = Ticket
        fields = [
            "title",
            "author",
            "release_date",
            "product_type",
            "description",
            "image",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class ReviewForm(forms.ModelForm):
    """review form"""

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

        widgets = {
            "body": forms.Textarea(attrs={"rows": 5}),
            "rating": forms.RadioSelect(attrs={"class": "inline"}),
        }

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


class TicketSearchByTitleForm(forms.Form):
    title = forms.CharField(
        max_length=128,
        label="Titre",
    )


class TicketSearchByAuthorForm(forms.Form):
    author = forms.CharField(
        max_length=128,
        label="Auteur",
    )


class TicketSearchByYear(forms.Form):
    year = forms.CharField(
        max_length=128,
        label="Année",
    )
