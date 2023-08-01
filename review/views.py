from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F, Case, When
from django.db import models
import flake8_html


from review.models import Ticket, Review
from review.forms import TicketForm, ReviewForm

FULL_STAR = "★"
EMPTY_STAR = "☆"


@login_required
def home(request):
    """homepage view"""

    # ordered by the most recent date between 'time_created' and 'time_edited'
    tickets = Ticket.objects.filter(user=request.user).order_by(
        Case(
            When(time_edited__gt=F("time_created"), then=F("time_edited")),
            default=F("time_created"),
            output_field=models.DateTimeField(),
        ).desc()
    )
    # ordered by the most recent date between 'time_created' and 'time_edited'
    reviews = Review.objects.filter(user=request.user).order_by(
        Case(
            When(time_edited__gt=F("time_created"), then=F("time_edited")),
            default=F("time_created"),
            output_field=models.DateTimeField(),
        ).desc()
    )

    return render(request, "review/home.html", {"tickets": tickets, "reviews": reviews})


@login_required
def posts(request):
    """posts view"""

    reviews = Review.objects.filter(user=request.user)

    return render(request, "review/posts.html", {"reviews": reviews})


@login_required
def ticket_list(request):
    """tickets list of current user"""

    # ordered by the most recent date between 'time_created' and 'time_edited'
    tickets = Ticket.objects.filter(user=request.user).order_by(
        Case(
            When(time_edited__gt=F("time_created"), then=F("time_edited")),
            default=F("time_created"),
            output_field=models.DateTimeField(),
        ).desc()
    )

    return render(request, "review/ticket_list.html", {"tickets": tickets})


@login_required
def ticket_detail(request, ticket_id):
    """ticket view"""

    ticket = get_object_or_404(Ticket, id=ticket_id)

    return render(request, "review/ticket_detail.html", {"ticket": ticket})


@login_required
def ticket_create(request):
    """ticket creation view"""

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            review = Review()
            ticket.user = request.user
            review.ticket = ticket
            ticket.save()
            review.save()

            return redirect("ticket_detail", ticket.id)

    else:
        form = TicketForm()

    return render(request, "review/ticket_create.html", {"form": form})


@login_required
def ticket_update(request, ticket_id):
    """ticket update view"""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = TicketForm(instance=ticket)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.time_edited = timezone.now()
            ticket.save()

            return redirect("ticket_detail", ticket.id)

    return render(request, "review/ticket_update.html", {"form": form})


@login_required
def ticket_delete(request, ticket_id):
    """ticket delete view"""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()

        return redirect("ticket_list")

    return render(request, "review/ticket_delete.html", {"ticket": ticket})


@login_required
def review_detail(request, review_id):
    """review view"""

    review = get_object_or_404(Review, id=review_id)

    return render(request, "review/review_detail.html", {"review": review})


@login_required
def review_create(request):
    """review creation view"""

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            review = review_form.save(commit=False)
            ticket.user = review.user = request.user
            ticket.time_created = review.time_created = timezone.now()
            review.ticket = ticket
            review.star = review.rating * FULL_STAR + (5 - review.rating) * EMPTY_STAR
            ticket.save()
            review.save()

            return redirect("posts")

    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(
        request,
        "review/review_create.html",
        {"ticket_form": ticket_form, "review_form": review_form},
    )
