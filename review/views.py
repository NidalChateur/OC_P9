from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F, Case, When, Q
from django.db import models
import flake8_html


from review.models import Ticket, Review, SelfReview
from review.forms import TicketForm, ReviewForm, SelfReviewForm




# en cours...(ajouter filtre post abonnement et self post)
@login_required
def home(request):
    """homepage view"""

    # ajouter les review des abonnements une fois réalisé.
    """     reviews = Review.objects.filter(
            Q(user=request.user) | Q(ticket__user=request.user)
        ).order_by("-time_last_entry") """

    reviews = Review.objects.all().order_by("-time_last_entry")

    return render(request, "review/home.html", {"reviews": reviews})


# OK
@login_required
def forbidden_permission(request):
    return render(request, "forbidden_permission.html")


# OK
@login_required
def posts(request):
    """posts view"""

    reviews = Review.objects.filter(
        Q(user=request.user) | Q(ticket__user=request.user)
    ).order_by("-time_last_entry")

    return render(request, "review/posts.html", {"reviews": reviews})


# inutile ?
@login_required
def ticket_list(request):
    """tickets list of the current user"""

    reviews = Review.objects.filter(ticket__user=request.user).order_by(
        "-time_last_entry"
    )

    return render(request, "review/ticket_list.html", {"reviews": reviews})


# OK inutile ?
@login_required
def ticket_detail(request, review_id):
    """ticket view"""

    review = get_object_or_404(Review, id=review_id)

    return render(request, "review/ticket_detail.html", {"review": review})


# OK
@login_required
def review_detail(request, review_id):
    """review detail view"""

    review = get_object_or_404(Review, id=review_id)

    return render(request, "review/review_detail.html", {"review": review})


# OK
@login_required
def ticket_create(request):
    """ticket creation view"""

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            review = Review()
            ticket = form.save(commit=False)
            ticket.user = request.user
            review.ticket = ticket
            ticket.save()
            review.save()

            return redirect("ticket_detail", review.id)

    else:
        form = TicketForm()

    return render(request, "review/ticket_create.html", {"form": form})


# OK
@login_required
def ticket_delete(request, ticket_id):
    """ticket delete view"""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user == request.user:
        if request.method == "POST":
            ticket.delete()

            return redirect("home")

        return render(request, "review/ticket_delete.html", {"ticket": ticket})

    return redirect("forbidden_permission")


# OK
@login_required
def ticket_update(request, ticket_id):
    """ticket update view"""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user == request.user:
        form = TicketForm(instance=ticket)
        if request.method == "POST":
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.save()

                return redirect("ticket_detail", ticket.id)

        return render(request, "review/ticket_update.html", {"form": form})

    return redirect("forbidden_permission")


# OK
@login_required
def ticket_self_review_create(request):
    """ticket and self review creation view"""

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        self_review_form = SelfReviewForm(request.POST)

        if all([ticket_form.is_valid(), self_review_form.is_valid()]):
            """Review() contains Ticket() and SelfReview() fields"""

            review = Review()

            ticket = ticket_form.save(commit=False)
            selfReview = self_review_form.save(commit=False)

            ticket.user = selfReview.user = request.user
            review.ticket = selfReview.ticket = ticket
            review.self_review = selfReview

            ticket.save()
            selfReview.save()
            review.save()

            return redirect("review_detail", review.id)

    else:
        ticket_form = TicketForm()
        self_review_form = SelfReviewForm()

    return render(
        request,
        "review/ticket_self_review_create.html",
        {"ticket_form": ticket_form, "review_form": self_review_form},
    )


# OK
@login_required
def self_review_create(request, review_id):
    """ self review creation """

    review = get_object_or_404(Review, id=review_id)

    if (review.ticket.user == request.user) and not review.self_review:
        if request.method == "POST":
            self_review_form = SelfReviewForm(request.POST)

            if self_review_form.is_valid():
                selfReview = self_review_form.save(commit=False)
                selfReview.user = request.user
                review.self_review = selfReview

                selfReview.save()
                review.save()

                return redirect("review_detail", review.id)

        else:
            self_review_form = SelfReviewForm()

        return render(
            request,
            "review/review_create.html",
            {"review_form": self_review_form, "review": review},
        )

    return redirect("forbidden_permission")


@login_required
def review_create(request, review_id):
    """ tierce review creation """

    review = get_object_or_404(Review, id=review_id)

    if (review.ticket.user != request.user) and not review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST)

            if review_form.is_valid():
                # tierce_review = review_form.save(commit=False)

                review.user = request.user
                review.rating = review_form.cleaned_data["rating"]
                review.headline = review_form.cleaned_data["headline"]
                review.body = review_form.cleaned_data["body"]

                review.save()

                return redirect("review_detail", review.id)

        else:
            review_form = ReviewForm()

        return render(
            request,
            "review/review_create.html",
            {"review_form": review_form, "review": review},
        )

    return redirect("forbidden_permission")

@login_required
def review_delete(request, review_id):
    """ delete tierce review """

    review = get_object_or_404(Review, id=review_id)

    if review.user == request.user:
        if request.method == "POST":
            review.user = None
            review.rating = None
            review.headline = None
            review.body = None

            review.save()

            return redirect("home")

        return render(request, "review/review_delete.html", {"review": review})

    return redirect("forbidden_permission")

@login_required
def self_review_delete(request, review_id):
    """ delete self review """

    review = get_object_or_404(Review, id=review_id)

    if review.self_review == request.user:
        if request.method == "POST":
            review.self_review = None

            review.save()

            return redirect("home")

        return render(request, "review/review_delete.html", {"review": review})

    return redirect("forbidden_permission")