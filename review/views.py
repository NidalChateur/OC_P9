from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from review.models import Ticket, Review
from review.forms import TicketForm, ReviewForm


@login_required
def home(request):
    """homepage view"""

    tickets = Ticket.objects.all()
    reviews = Review.objects.all()

    return render(request, "review/home.html", {"tickets": tickets, "reviews": reviews})


def ticket_create(request):
    """ticket creation view"""

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()

        return redirect("home")

    else:
        form = TicketForm()

    return render(request, "review/ticket_create.html", {"form": form})

def review_create(request):
    """review creation view"""

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            ticket = form.save()

        return redirect("home")

    else:
        form = ReviewForm()

    return render(request, "review/review_create.html", {"form": form})
