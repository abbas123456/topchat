from django.views import generic
from client import models
from django import http
from client.forms import RoomForm
from django.core.urlresolvers import reverse
from django.contrib import messages


class DashboardViewMixin(object):

    def get_room_from_url(self):
        if 'room' in self.request.GET:
            room = self.request.GET['room']
            return models.Room.objects.get(id=room)
        else:
            return None

    def get_object(self, queryset=None):
        if self.get_room_from_url() is None:
            return models.Room()
        else:
            return self.get_room_from_url()

    def get(self, request, *args, **kwargs):
        room = self.get_room_from_url()
        if room is not None and room.created_by != request.user:
            return http.HttpResponseForbidden()
        return super(DashboardViewMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        room = self.get_room_from_url()
        if room is not None and room.created_by != request.user:
            return http.HttpResponseRedirect(reverse('dashboard_general'))
        elif room is None:
            return http.HttpResponseRedirect(reverse('dashboard_general'))
        return super(DashboardViewMixin, self).post(request, *args, **kwargs)


class GeneralPageView(DashboardViewMixin, generic.UpdateView):
    template_name = 'dashboard/general_page.html'
    form_class = RoomForm

    def form_valid(self, form):
        messages.success(self.request, "Your changes have been saved")
        return super(GeneralPageView, self).form_valid(form)

    def get_success_url(self):
        return "{0}?room={1}".format(reverse('dashboard_general'),
                                     self.get_object().id)


class AppearancePageView(generic.TemplateView):
    template_name = 'dashboard/appearance_page.html'


class AdministratorsPageView(generic.TemplateView):
    template_name = 'dashboard/administrators_page.html'


class UserManagementPageView(generic.TemplateView):
    template_name = 'dashboard/user_management_page.html'


class YourWebsitePageView(generic.TemplateView):
    template_name = 'dashboard/your_website_page.html'


class DeleteRoomView(DashboardViewMixin, generic.DeleteView):
    template_name = 'dashboard/delete_room.html'

    def get_success_url(self):
        return reverse('dashboard_general')
