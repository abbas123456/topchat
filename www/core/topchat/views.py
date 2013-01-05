from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from core.topchat.models import HoldingPageNotification


class HomePageView(TemplateView):
    template_name = 'topchat/home.html'


class AboutPageView(TemplateView):
    template_name = 'topchat/about.html'


class GetStartedPageView(TemplateView):
    template_name = 'topchat/get_started.html'


class HoldingPageView(CreateView):
    model = HoldingPageNotification

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. We'll be in touch.")
        return HttpResponseRedirect(reverse('holding'))
