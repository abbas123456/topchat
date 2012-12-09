from django import template
from django.template import Context
from django.template.loader import render_to_string
from client.models import Room

register = template.Library()

@register.simple_tag(takes_context=True)
def render_navigation_bar(context):
    request = context['request']
    context['rooms'] = Room.objects.filter(created_by=request.user)
    return render_to_string("dashboard/navigation_bar.html", Context(context))
