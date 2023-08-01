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


def profile(request):
    """profile view"""

    return render(request, "authentication/profile.html")


def profile_update(request):
    """profile update view"""

    form = forms.ProfileForm(instance=request.user)
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")

    return render(request, "authentication/profile_update.html", {"form": form})
