from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """homepage view"""

    return render(request, "review/home.html")
