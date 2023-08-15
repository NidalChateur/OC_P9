from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F, Case, When, Q
from django.db import models
from django.forms import formset_factory
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.text import slugify

from imp import get_frozen_object

from authentication.models import User
from review.models import Ticket, Review, Follower
from review.forms import TicketForm, ReviewForm, FollowerForm
from review.validators import validate_followed_user

""" # exemple pagination
@login_required
def home(request):
    blogs = models.Blog.objects.filter(
        Q(contributors__in=request.user.follows.all()) | Q(starred=True)
    )
    photos = models.Photo.objects.filter(
        uploader__in=request.user.follows.all()
    ).exclude(blog__in=blogs)

    blogs_and_photos = sorted(
        chain(blogs, photos), key=lambda instance: instance.date_created, reverse=True
    )
    # 1. on instancie paginator
    paginator = Paginator(blogs_and_photos, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # 2. on passe page_obj au contexte
    context = {"page_obj": page_obj}

    return render(request, "blog/home.html", context=context)
 """


# en cours...(ajouter la pagination)
@login_required
def home(request):
    """homepage view"""

    # requête inversée ? ici
    followed_users = Follower.objects.filter(user=request.user).values_list(
        "followed_user", flat=True
    )
    reviews = Review.objects.filter(
        (Q(is_self_review=False))
        & (
            Q(user=request.user)
            | Q(ticket__user=request.user)
            | Q(user__in=followed_users)
            | Q(ticket__user__in=followed_users)
        )
    ).order_by("-time_last_entry")

    return render(request, "review/home.html", {"reviews": reviews})


# OK
@login_required
def forbidden_permission(request):
    return render(request, "forbidden_permission.html")


# en cours...(ajouter la pagination)
@login_required
def posts(request):
    """posts view"""

    reviews = Review.objects.filter(
        Q(is_self_review=False) & (Q(user=request.user) | Q(ticket__user=request.user))
    ).order_by("-time_last_entry")

    return render(request, "review/posts.html", {"reviews": reviews})


# en cours...(ajouter la pagination)
@login_required
def ticket_list(request):
    """tickets list of the current user"""

    reviews = Review.objects.filter(is_self_review=False).order_by("-time_last_entry")

    return render(request, "review/ticket_list.html", {"reviews": reviews})


# OK
@login_required
def ticket_detail(request, ticket_id):
    """ticket view"""

    review = get_object_or_404(Review, ticket__id=ticket_id, is_self_review=False)

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

            if Ticket.objects.filter(slug=slugify(ticket.title)):
                existant_ticket=Ticket.objects.get(slug=slugify(ticket.title))
                messages.info(request, " ⚠️ Demande de critique déjà existante")
                return redirect("ticket_detail", existant_ticket.id)

            ticket.save()
            review.save()

            messages.success(request, " ✅ Demande de critique crée avec succès !")

            return redirect("ticket_detail", ticket.id)

    else:
        form = TicketForm()

    return render(request, "review/ticket_create.html", {"form": form})


# OK
@login_required
def ticket_delete(request, ticket_id):
    """ticket delete view"""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        return redirect("forbidden_permission")
    
    if request.method == "POST":
        ticket.delete()
        messages.success(request, " ✅ Demande de critique supprimée avec succès !")

        return redirect("home")

    return render(request, "review/ticket_delete.html", {"ticket": ticket})



# OK
@login_required
def ticket_update(request, ticket_id):
    """ticket update view"""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    review = get_object_or_404(Review, ticket__id=ticket_id, is_self_review=False)

    if ticket.user != request.user:
        return redirect("forbidden_permission")
    
    form = TicketForm(instance=ticket)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save()
            review.save()

            messages.success(
                request, " ✅ Demande de critique modifiée avec succès !"
            )

            return redirect("ticket_detail", ticket.id)

    return render(request, "review/ticket_update.html", {"form": form})

    


# OK
@login_required
def ticket_self_review_create(request):
    """ticket and self review creation view"""

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        self_review_form = ReviewForm(request.POST)

        if all([ticket_form.is_valid(), self_review_form.is_valid()]):
            review = Review()

            ticket = ticket_form.save(commit=False)
            selfReview = self_review_form.save(commit=False)

            ticket.user = selfReview.user = request.user
            review.ticket = selfReview.ticket = ticket
            review.self_review = selfReview

            if Ticket.objects.filter(slug=slugify(ticket.title)):
                existant_ticket=Ticket.objects.get(slug=slugify(ticket.title))
                messages.info(request, " ⚠️ Demande de critique déjà existante")
                
                return redirect("ticket_detail", existant_ticket.id)

            ticket.save()
            selfReview.save()
            review.save()

            messages.success(request, " ✅ Demande de critique crée avec succès !")

            return redirect("review_detail", review.id)

    else:
        ticket_form = TicketForm()
        self_review_form = ReviewForm()

    return render(
        request,
        "review/ticket_self_review_create.html",
        {"ticket_form": ticket_form, "review_form": self_review_form},
    )


# OK
@login_required
def self_review_create(request, review_id):
    """self review creation"""

    review = get_object_or_404(Review, id=review_id)

    if (review.ticket.user != request.user) or review.self_review:
        return redirect("forbidden_permission")
    
    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            selfReview = form.save(commit=False)
            selfReview.user = request.user
            selfReview.ticket = review.ticket
            review.self_review = selfReview

            selfReview.save()
            review.save()

            messages.success(request, " ✅ Critique crée avec succès !")

            return redirect("review_detail", review.id)

    else:
        form = ReviewForm()

    return render(
        request,
        "review/review_create.html",
        {"form": form, "review": review},
    )

    


# OK
@login_required
def self_review_delete(request, review_id):
    """delete self review"""

    review = get_object_or_404(Review, id=review_id)

    if review.self_review.user != request.user:
        return redirect("forbidden_permission")
    
    if request.method == "POST":
        review.self_review.delete()

        if review.headline:
            messages.success(request, " ✅ Critique supprimée avec succès !")

            return redirect("review_detail", review.id)
        
        messages.success(request, " ✅ Critique supprimée avec succès !")

        return redirect("ticket_detail", review.ticket.id)

    return render(request, "review/review_delete.html", {"review": review})



# OK
@login_required
def self_review_update(request, review_id):
    """self review update"""

    review = get_object_or_404(Review, id=review_id)

    if review.self_review.user != request.user:
        return redirect("forbidden_permission")
    
    form = ReviewForm(instance=review.self_review)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review.self_review)
        if form.is_valid():
            form.save()
            review.save()

            messages.success(request, " ✅ Critique modifiée avec succès !")

            return redirect("review_detail", review.id)

    return render(
        request, "review/review_update.html", {"review": review, "form": form}
    )



# OK
@login_required
def review_create(request, review_id):
    """tierce review creation"""

    review = get_object_or_404(Review, id=review_id)

    if (review.ticket.user != request.user) and not review.user:
        if request.method == "POST":
            form = ReviewForm(request.POST)

            if form.is_valid():
                review.user = request.user
                review.rating = form.cleaned_data["rating"]
                review.headline = form.cleaned_data["headline"]
                review.body = form.cleaned_data["body"]

                review.save()

                messages.success(request, " ✅ Critique crée avec succès !")

                return redirect("review_detail", review.id)

        else:
            form = ReviewForm()

        return render(
            request,
            "review/review_create.html",
            {"form": form, "review": review},
        )

    return redirect("forbidden_permission")


# OK
@login_required
def review_delete(request, review_id):
    """delete tierce review"""

    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect("forbidden_permission")
    
    if request.method == "POST":
        review.set_null()

        if review.self_review:
            messages.success(request, " ✅ Critique supprimée avec succès !")

            return redirect("review_detail", review.id)
        
        messages.success(request, " ✅ Critique supprimée avec succès !")

        return redirect("ticket_detail", review.ticket.id)

    return render(request, "review/review_delete.html", {"review": review})



# OK
@login_required
def review_update(request, review_id):
    """review update"""

    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect("forbidden_permission")
    
    form = ReviewForm(instance=review)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()

            messages.success(request, " ✅ Critique modifiée avec succès !")

            return redirect("review_detail", review.id)

    return render(
        request, "review/review_update.html", {"review": review, "form": form}
    )



# OK (ajouter bloquer un utilisateur ?)
@login_required
def follower(request):
    follow = Follower()
    form = FollowerForm()
    followed_users = Follower.objects.filter(user=request.user)
    followers = Follower.objects.filter(followed_user=request.user)

    if request.method == "POST":
        form = FollowerForm(request.POST)
        if form.is_valid():

            if request.user.username == form.cleaned_data["followed_user"]:
                messages.error(request, " 🚫 Abonnement non autorisé !")

                return redirect("follower")

            follow.user = request.user
            follow.followed_user = User.objects.get(
                username=form.cleaned_data["followed_user"]
            )

            if Follower.objects.filter(
                user=request.user, followed_user=follow.followed_user
            ):
                messages.error(request, " 🚫 Abonnement déjà existant !")

                return redirect("follower")

            follow.save()

            messages.success(
                request,
                f" ✅ Abonnement à {follow.followed_user} crée avec succès !",
            )

            return redirect("follower")

    return render(
        request,
        "review/follower.html",
        {
            "form": form,
            "followed_users": followed_users,
            "followers": followers,
        },
    )


# OK
@login_required
def follower_delete(request, follower_id):
    follower = Follower.objects.get(id=follower_id)

    if request.user != follower.user:
        return redirect("forbidden_permission")

    followed_user = follower.followed_user
    follower.delete()

    messages.success(request, f" ✅ Abonnement à {followed_user} supprimé avec succès !")

    return redirect("follower")
