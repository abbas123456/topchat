from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'mochatapp/home.html'

class AboutPageView(TemplateView):
    template_name = 'mochatapp/about.html'
