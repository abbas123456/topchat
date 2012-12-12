from django import template
from django.template import Context
from django.template.loader import render_to_string
from client.models import Room
from django.core.urlresolvers import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def render_navigation_bar(context):
    request = context['request']
    context['rooms'] = Room.objects.filter(created_by=request.user)
    context['current_url'] = resolve(request.get_full_path()).url_name
    return render_to_string("dashboard/navigation_bar.html", Context(context))
