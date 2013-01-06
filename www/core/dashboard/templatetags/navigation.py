from django import template
from django.template import Context
from django.template.loader import render_to_string
from core.client.models import Room
from django.core.urlresolvers import resolve

register = template.Library()


@register.inclusion_tag("dashboard/navigation_bar.html", takes_context=True)
def render_navigation_bar(context):
    request = context['request']
    context['rooms'] = Room.objects.filter(created_by=request.user)
    context['current_url'] = resolve(request.get_full_path()).url_name
    if 'room' in request.GET:
        room_number = int(request.GET['room'])
        context['has_room_selected'] = True
        context['current_room'] = room_number
    else:
        context['has_room_selected'] = False
    return context


@register.simple_tag(takes_context=True)
def has_room_selected(context):
    request = context['request']
    return 'room' in request.GET
