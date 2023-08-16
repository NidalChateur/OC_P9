from django.contrib import admin

from review.models import Ticket, Review, Relation


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


class RelationAdmin(admin.ModelAdmin):
    list_display = (
        "user_1",
        "type",
        "user_2",
        "description",
        "id"
    )


admin.site.register(Relation, RelationAdmin)
