from django import template
from django.utils import timezone

from review.models import Review, Ticket


MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()

""" syntaxe in template : 
{{ instance.field_name|filter_name }}"""


@register.filter(name="is_instance_of_ticket")
def is_instance_of_ticket(obj) -> bool:
    return isinstance(obj, Ticket)


@register.filter(name="is_instance_of_review")
def is_instance_of_review(obj) -> bool:
    return isinstance(obj, Review)


@register.filter
def model_type(value):
    """retourne le nom d'un type ("Blog" ou "Photo")"""

    return type(value).__name__


@register.filter
def is_recent(posted_at: timezone) -> bool:
    return (timezone.now() - posted_at).total_seconds() <= DAY


@register.filter
def get_posted_at_display(posted_at: timezone) -> str:
    # difference between now and posted_at in secs
    seconds_ago = (timezone.now() - posted_at).total_seconds()

    if seconds_ago <= MINUTE:
        return "il y a moins d'une minute"

    elif seconds_ago <= HOUR:
        return f"il y a {int(seconds_ago // MINUTE)} minutes"

    elif seconds_ago < 2 * HOUR:
        return "il y a une heure"

    return f"il y a {int(seconds_ago // HOUR)} heures."


""" syntaxe in template :
{% filter_name instance.field_name %}"""


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if context["user"] == user:
        """affiche vous ou le nom de l'utilisateur tiers
        à la place d'afficher toujours le nom de l'utilisateur"""

        return "Vous"

    return user.username
