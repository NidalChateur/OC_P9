from django import template
from django.utils import timezone


MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()

""" syntaxe in template : 
{{ instance.field_name|filter_name }}"""


@register.filter
def is_recent(posted_at: timezone) -> bool:
    """posted today or not"""

    return (timezone.now() - posted_at).total_seconds() <= DAY


@register.filter
def get_posted_at_display(posted_at: timezone) -> str:
    """difference between now and posted_at in secs"""

    seconds_ago = (timezone.now() - posted_at).total_seconds()

    if seconds_ago <= MINUTE:
        return "il y a moins d'une minute"

    elif seconds_ago <= HOUR:
        return f"il y a {int(seconds_ago // MINUTE)} minutes"

    elif seconds_ago < 2 * HOUR:
        return "il y a une heure"

    return f"il y a {int(seconds_ago // HOUR)} heures."
