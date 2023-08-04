from django.urls import path

from review.views import (
    home,
    posts,
    ticket_list,
    ticket_detail,
    ticket_create,
    ticket_update,
    ticket_delete,
    review_detail,
    ticket_self_review_create,
    forbidden_permission,
    self_review_create,
    review_create,
    review_delete,
    self_review_delete
)


urlpatterns = [
    # ticket & review
    path("home/", home, name="home"),
    path("posts/", posts, name="posts"),
    path("reviews/ticket_self_review_create/", ticket_self_review_create, name="ticket_self_review_create"),
    path("forbidden_permission/", forbidden_permission, name="forbidden_permission"),
    # ticket
    path("tickets/", ticket_list, name="ticket_list"),
    path("tickets/<int:review_id>/", ticket_detail, name="ticket_detail"),
    path("tickets/create/", ticket_create, name="ticket_create"),
    path("tickets/<int:ticket_id>/update/", ticket_update, name="ticket_update"),
    path("tickets/<int:ticket_id>/delete/", ticket_delete, name="ticket_delete"),
    # review
    path("reviews/<int:review_id>/", review_detail, name="review_detail"),
    path("reviews/<int:review_id>/self_review_create/", self_review_create, name="self_review_create"),
    path("reviews/<int:review_id>/review_create/", review_create, name="review_create"),
    path("reviews/<int:review_id>/review_delete/", review_delete, name="review_delete"),
    path("reviews/<int:review_id>/self_review_delete/", self_review_delete, name="self_review_delete"),
]
