from django.contrib import admin

from review.models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "time_last_entry",
        "time_created",
        "time_edited",
        "id",
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
        "self_review_instance",
    )


admin.site.register(Review, ReviewAdmin)
