from django.shortcuts import render, redirect
from django.contrib.auth import login

# best way to import settings.py file
from django.conf import settings

from authentication import forms


def signup(request):
    """signup view"""

    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            # save the user in DB
            user = form.save()
            # auto-login user
            login(request, user)

            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "authentication/signup.html", {"form": form})
