from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.text import slugify


from authentication.models import User
from review.models import Ticket, Review, Relation
from review.forms import (
    TicketForm,
    ReviewForm,
    RelationForm,
    TicketSearchByTitleForm,
    TicketSearchByAuthorForm,
    TicketSearchByYear,
)


def paginator(request, qs) -> Paginator:
    paginator = Paginator(qs, 6)
    page_number = request.GET.get("page")

    return paginator.get_page(page_number)


@login_required
def forbidden_permission(request):
    return render(request, "forbidden_permission.html")


@login_required
def home(request):
    """homepage view.
    read tickets and reviews posted by the connected user and the users he follows"""

    followed_users = Relation.objects.filter(
        user_1=request.user, type="follows"
    ).values_list("user_2", flat=True)

    reviews = Review.objects.filter(
        (Q(is_self_review=False))
        & (
            Q(user=request.user)
            | Q(ticket__user=request.user)
            | Q(user__in=followed_users)
            | Q(ticket__user__in=followed_users)
        )
    ).order_by("-time_last_entry")

    page_obj = paginator(request, reviews)

    return render(request, "review/home.html", {"page_obj": page_obj})


@login_required
def posts(request):
    """posts view.
    read tickets and reviews posted by the connected user"""

    reviews = Review.objects.filter(
        Q(is_self_review=False) & (Q(user=request.user) | Q(ticket__user=request.user))
    ).order_by("-time_last_entry")

    page_obj = paginator(request, reviews)

    return render(request, "review/posts.html", {"page_obj": page_obj})


@login_required
def ranking(request):
    """ranking view.
    read all tickets ordered by rating"""

    reviews = Review.objects.filter(is_self_review=False).order_by("-overall_rating")

    page_obj = paginator(request, reviews)

    return render(request, "review/ranking.html", {"page_obj": page_obj})


@login_required
def ticket_detail(request, ticket_id):
    """ticket view
    Display a ticket and its reviews using the ticket_id field"""

    review = get_object_or_404(Review, ticket__id=ticket_id, is_self_review=False)

    # Test if the connected user is blocked by the user who created the ticket
    if Relation.objects.filter(
        user_1=review.ticket.user, type="blocks", user_2=request.user
    ):
        return redirect("forbidden_permission")

    return render(request, "review/ticket_detail.html", {"review": review})


@login_required
def review_detail(request, review_id):
    """review detail view
    Display a ticket and its reviews using the review_id field"""

    review = get_object_or_404(Review, id=review_id)

    # Test if the connected user is blocked by the user who created the ticket
    if Relation.objects.filter(
        user_1=review.ticket.user, type="blocks", user_2=request.user
    ):
        return redirect("forbidden_permission")

    return render(request, "review/review_detail.html", {"review": review})


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

            if Ticket.objects.filter(slug_title=slugify(ticket.title)):
                existant_ticket = get_object_or_404(
                    Ticket, slug_title=slugify(ticket.title)
                )
                messages.info(request, " ⚠️ Demande de critique déjà existante")

                return redirect("ticket_detail", existant_ticket.id)

            ticket.save()
            review.save()

            messages.success(request, " ✅ Demande de critique crée avec succès !")

            return redirect("ticket_detail", ticket.id)

    else:
        form = TicketForm()

    return render(request, "review/ticket_create.html", {"form": form})


@login_required
def ticket_delete(request, ticket_id):
    """ticket deletion view"""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        return redirect("forbidden_permission")

    if request.method == "POST":
        ticket.delete()
        messages.success(request, " ✅ Demande de critique supprimée avec succès !")

        return redirect("home")

    return render(request, "review/ticket_delete.html", {"ticket": ticket})


@login_required
def ticket_update(request, ticket_id):
    """ticket updating view"""

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

            messages.success(request, " ✅ Demande de critique modifiée avec succès !")

            return redirect("ticket_detail", ticket.id)

    return render(request, "review/ticket_update.html", {"form": form})


@login_required
def ticket_self_review_create(request):
    """ticket and self review creation view
    when the ticket author is also the review author :
    the review is tagged as a self_review"""

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

            if Ticket.objects.filter(slug_title=slugify(ticket.title)):
                existant_ticket = get_object_or_404(
                    Ticket, slug_title=slugify(ticket.title)
                )
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


@login_required
def self_review_create(request, review_id):
    """self review creation view
    when the ticket author is also the review author :
    the review is tagged as a self_review"""

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


@login_required
def self_review_delete(request, review_id):
    """self review deletion view"""

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


@login_required
def self_review_update(request, review_id):
    """self review updating view"""

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


@login_required
def review_create(request, review_id):
    """tierce review creation view
    when the ticket author and the review author are different
    """

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


@login_required
def review_delete(request, review_id):
    """tierce review deletion view"""

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


@login_required
def review_update(request, review_id):
    """review updating view"""

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


@login_required
def relation(request):
    """create and read relations
    a relation is:
    - user_1 follows or blocks user_2"""

    relation = Relation()
    form = RelationForm()
    followed_users = Relation.objects.filter(user_1=request.user, type="follows")
    followers = Relation.objects.filter(user_2=request.user, type="follows")
    blocked_users = Relation.objects.filter(user_1=request.user, type="blocks")

    if request.method == "POST":
        form = RelationForm(request.POST)
        if form.is_valid():
            # test if the entered user exists
            try:
                user = User.objects.get(username=form.cleaned_data["followed_user"])
            except User.DoesNotExist:
                messages.error(request, " 🚫 Cet utilisateur n'existe pas !")

                return redirect("relation")

            # test if the connected user the entered user are different
            if request.user.username == user.username:
                messages.error(request, " 🚫 Abonnement non autorisé !")

                return redirect("relation")

            # test if the relation is already created
            if Relation.objects.filter(
                user_1=request.user, type="follows", user_2=user
            ):
                messages.error(request, " 🚫 Abonnement déjà existant !")

                return redirect("relation")

            # test if the connected user does not block the entered user
            if Relation.objects.filter(user_1=request.user, type="blocks", user_2=user):
                messages.error(
                    request,
                    " 🚫 Utilisateur bloqué ! Veuillez le débloquer avant de pouvoir le suivre.",
                )

                return redirect("relation")

            # test if the entered user does not block the connected user
            if Relation.objects.filter(user_1=user, type="blocks", user_2=request.user):
                messages.error(request, " 🚫 Abonnement non autorisé !")

                return redirect("relation")

            relation.user_1 = request.user
            relation.type = "follows"
            relation.user_2 = user
            relation.save()

            messages.success(
                request,
                f" ✅ Abonnement à {relation.user_2} crée avec succès !",
            )

            return redirect("relation")

    return render(
        request,
        "review/relation.html",
        {
            "form": form,
            "followed_users": followed_users,
            "followers": followers,
            "blocked_users": blocked_users,
        },
    )


@login_required
def relation_delete(request, relation_id):
    """delete a relation"""

    relation = get_object_or_404(Relation, id=relation_id)

    if relation.user_1 != request.user:
        return redirect("forbidden_permission")

    deleted_user = relation.user_2
    relation_type = relation.type
    relation.delete()

    if relation_type == "follows":
        messages.success(
            request, f" ✅ Abonnement à {deleted_user} supprimé avec succès !"
        )
    else:
        messages.success(request, f" ✅ {deleted_user} à été débloqué avec succès !")

    return redirect("relation")


@login_required
def relation_block(request, relation_id):
    """change "user_1 follows user_2" to
    user_2 blocks user_1"""

    relation = get_object_or_404(Relation, id=relation_id)

    if relation.user_2 != request.user:
        return redirect("forbidden_permission")

    blocked_user = relation.user_1

    relation.user_1 = request.user
    relation.type = "blocks"
    relation.user_2 = blocked_user
    relation.save()

    messages.success(request, f" ✅ Vous avez bloqué {blocked_user} !")

    return redirect("relation")


@login_required
def search(request):
    search_by_title_form = TicketSearchByTitleForm()
    search_by_author_form = TicketSearchByAuthorForm()
    search_by_year_form = TicketSearchByYear()

    if request.method == "POST":
        if "title" in request.POST:
            search_by_title_form = TicketSearchByTitleForm(request.POST)
            if search_by_title_form.is_valid():
                title = search_by_title_form.cleaned_data["title"]
                if Review.objects.filter(ticket__slug_title=slugify(title)):
                    qs = Review.objects.filter(
                        ticket__slug_title=slugify(title), is_self_review=False
                    )
                    messages.success(
                        request,
                        f" ✅  {len(qs)} résultat(s) trouvé(s) !",
                    )
                    page_obj = paginator(request, qs)

                    return render(request, "review/home.html", {"page_obj": page_obj})

                messages.error(request, " ❌ Aucun résultat trouvé !")

                return redirect("search")

        if "author" in request.POST:
            search_by_author_form = TicketSearchByAuthorForm(request.POST)
            if search_by_author_form.is_valid():
                author = search_by_author_form.cleaned_data["author"]
                if Review.objects.filter(ticket__slug_author=slugify(author)):
                    qs = Review.objects.filter(
                        ticket__slug_author=slugify(author), is_self_review=False
                    )
                    messages.success(
                        request,
                        f" ✅  {len(qs)} résultat(s) trouvé(s)",
                    )
                    page_obj = paginator(request, qs)

                    return render(request, "review/home.html", {"page_obj": page_obj})

                messages.error(request, " ❌ Aucun résultat trouvé !")

                return redirect("search")

        if "year" in request.POST:
            search_by_year_form = TicketSearchByYear(request.POST)
            if search_by_year_form.is_valid():
                year = search_by_year_form.cleaned_data["year"]
                if Review.objects.filter(ticket__release_date=year):
                    qs = Review.objects.filter(
                        ticket__release_date=year, is_self_review=False
                    )
                    messages.success(
                        request,
                        f" ✅  {len(qs)} résultat(s) trouvé(s)",
                    )
                    page_obj = paginator(request, qs)

                    return render(request, "review/home.html", {"page_obj": page_obj})

                messages.error(request, " ❌ Aucun résultat trouvé !")

                return redirect("search")

    return render(
        request,
        "review/search.html",
        {
            "search_by_title_form": search_by_title_form,
            "search_by_author_form": search_by_author_form,
            "search_by_year_form": search_by_year_form,
        },
    )
