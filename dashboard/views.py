from django.views.generic import ListView
from client.models import Room


class HomePageView(ListView):
    template_name = 'dashboard/home_page.html'

    def get_queryset(self):
        return Room.objects.filter(created_by=self.request.user)
