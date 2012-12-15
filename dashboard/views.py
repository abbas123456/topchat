from django.views import generic
from client import models


class GeneralPageView(generic.TemplateView):
    template_name = 'dashboard/general_page.html'


class AppearancePageView(generic.TemplateView):
    template_name = 'dashboard/appearance_page.html'


class AdministratorsPageView(generic.TemplateView):
    template_name = 'dashboard/administrators_page.html'
