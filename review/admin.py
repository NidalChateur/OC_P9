from django.contrib import admin

from review.models import Ticket, Review, SelfReview


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "time_created", "id")


admin.site.register(Ticket, TicketAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "ticket", "time_created", "time_edited", "id")


admin.site.register(Review, ReviewAdmin)


class SelfReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "ticket", "time_created", "time_edited", "id")


admin.site.register(SelfReview, SelfReviewAdmin)
