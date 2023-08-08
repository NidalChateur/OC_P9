""" crée un filtre utilisable dans un template ! """
from review.models import Review, Ticket
from django import template


register = template.Library()


@register.filter(name="is_instance_of_ticket")
def is_instance_of_ticket(obj):
    return isinstance(obj, Ticket)


@register.filter(name="is_instance_of_review")
def is_instance_of_review(obj):
    return isinstance(obj, Review)
