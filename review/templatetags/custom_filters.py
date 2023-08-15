""" crée un filtre utilisable dans un template ! 
utilisable uniquement dans un template de l'app review..."""

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
def is_instance_of_ticket(obj):
    return isinstance(obj, Ticket)


@register.filter(name="is_instance_of_review")
def is_instance_of_review(obj):
    return isinstance(obj, Review)


# début filtre du cours
@register.filter
def model_type(value):
    """retourne le nom d'un type ("Blog" ou "Photo")"""

    return type(value).__name__


@register.filter
def get_posted_at_display(posted_at):
    # fait la différence entre le temps de maintenant et le temps
    # de l'instance et retourne le résultat en seconde
    seconds_ago = (timezone.now() - posted_at).total_seconds()
    # si l'instance à été crée il y a moins d'une heure
    if seconds_ago <= HOUR:
        return f"Publié il y a {int(seconds_ago // MINUTE)} minutes."
    # si l'instance à été crée il y moins de 24h
    elif seconds_ago <= DAY:
        return f"Publié il y a {int(seconds_ago // HOUR)} heures."
    # posté il y a plus d'un jour, retourne la date
    return f'Publié le {posted_at.strftime("%d %b %y à %Hh%M")}'


""" syntaxe in template :
{% filter_name instance.field_name %}"""


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if context["user"] == user:
        """affiche vous ou le nom de l'utilisateur tiers
        à la place d'afficher toujours le nom de l'utilisateur"""

        return "Vous"

    return user.username
