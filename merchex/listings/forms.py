# listings/forms.py

from django import forms


class ContactUsForm(forms.Form):
    """création du formulaire de contact"""

    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)
