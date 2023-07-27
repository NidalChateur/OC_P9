from django.contrib import admin

from review.models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "time_created")


admin.site.register(Ticket, TicketAdmin)
