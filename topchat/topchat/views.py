from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'topchat/home.html'

class AboutPageView(TemplateView):
    template_name = 'topchat/about.html'

class GettingStartedPageView(TemplateView):
    template_name = 'topchat/getting_started.html'

class HoldingPageView(TemplateView):
    template_name = 'topchat/holding.html'
