from django.views.generic import TemplateView
from client.models import Room

class HomePageView(TemplateView):
    template_name = 'mochatapp/home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['active_rooms'] = Room.objects.all()[0:3]
        return context

class AboutPageView(TemplateView):
    template_name = 'mochatapp/about.html'
