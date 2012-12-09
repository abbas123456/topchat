from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'dashboard/home_page.html'
