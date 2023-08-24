from tkinter import Widget
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
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "release_date": forms.NumberInput(attrs={"class": "form-control"}),
            "product_type": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class ReviewForm(forms.ModelForm):
    """review form"""

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

        widgets = {
            "headline": forms.TextInput(attrs={"class": "form-control"}),
            "rating": forms.RadioSelect(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
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
