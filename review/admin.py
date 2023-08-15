from django.contrib import admin

from review.models import Ticket, Review, Follower


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "time_created",
        "time_edited",
        "id",
        "slug"
    )


admin.site.register(Ticket, TicketAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "ticket",
        "time_last_entry",
        "time_created",
        "time_edited",
        "id",
        "is_self_review"
    )


admin.site.register(Review, ReviewAdmin)


class FollowerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "followed_user",
        "description",
        "id"
    )


admin.site.register(Follower, FollowerAdmin)
