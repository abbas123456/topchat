from django.views import generic
from client import models
from django import http
from dashboard import forms
from client.models import Room
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.core.exceptions import ValidationError


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

    def form_valid(self, form):
        messages.success(self.request, "Your changes have been saved")
        return super(DashboardViewMixin, self).form_valid(form)


class GeneralPageView(DashboardViewMixin, generic.UpdateView):
    template_name = 'dashboard/general_page.html'
    form_class = forms.RoomForm

    def get_success_url(self):
        return "{0}?room={1}".format(reverse('dashboard_general'),
                                     self.get_object().id)


class AppearancePageView(DashboardViewMixin, generic.UpdateView):
    template_name = 'dashboard/appearance_page.html'

    def get_object(self, queryset=None):
        room = super(AppearancePageView, self).get_object()
        if room.id is not None:
            return room.appearance
        return super(AppearancePageView, self).get_object()

    def get_success_url(self):
        return "{0}?room={1}".format(reverse('dashboard_appearance'),
                                     super(AppearancePageView,
                                           self).get_object().id)


class AdministratorsPageView(DashboardViewMixin, generic.TemplateView):
    template_name = 'dashboard/administrators_page.html'
    AdministratorFormSet = modelformset_factory(models.RoomAdministrator,
                                                form=forms.RoomAdministratorForm,
                                                can_delete=True)

    def get_context_data(self, **kwargs):
        context = super(AdministratorsPageView, self).get_context_data(**kwargs)
        room = self.get_object()
        if room.id is not None:
            queryset = models.RoomAdministrator.objects.filter(room_id=room.id)
            context['formset'] = self.AdministratorFormSet(queryset=queryset)
        return context

    def post(self, request, *args, **kwargs):
        room = self.get_room_from_url()
        if room is not None and room.created_by != request.user:
            return http.HttpResponseRedirect(reverse('dashboard_general'))
        elif room is None:
            return http.HttpResponseRedirect(reverse('dashboard_general'))
        formset = self.AdministratorFormSet(request.POST, request.FILES)
        if formset.is_valid():
            administrators = formset.save(commit=False)
            for administrator in administrators:
                administrator.room = room
                try:
                    administrator.full_clean()
                    administrator.save()
                except ValidationError as e:
                    messages.error(self.request, e.message_dict['__all__'][0])
                    return http.HttpResponseRedirect(self.get_success_url())

            messages.success(self.request, "Your changes have been saved")
        else:
            messages.error(self.request, "Your changes could not be saved")

        return http.HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "{0}?room={1}".format(reverse('dashboard_administrators'),
                                     super(AdministratorsPageView,
                                           self).get_object().id)


class UserManagementPageView(generic.TemplateView):
    template_name = 'dashboard/user_management_page.html'


class YourWebsitePageView(DashboardViewMixin, generic.DetailView):
    template_name = 'dashboard/your_website_page.html'

    def get_context_data(self, **kwargs):
        context = super(YourWebsitePageView, self).get_context_data(**kwargs)
        if self.get_object().id is not None:
            hostname = self.request.get_host()
            path = reverse('standalone_room_detail',
                           kwargs={'pk': self.get_object().id})
            context['room_standalone_url'] = "{0}{1}".format(hostname, path)
        return context


class DeleteRoomView(DashboardViewMixin, generic.DeleteView):
    template_name = 'dashboard/delete_room.html'

    def get_success_url(self):
        return reverse('dashboard_general')


class CreateRoomView(generic.CreateView):
    model = Room
    form_class = forms.RoomForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.is_active = True
        appearance = models.RoomAppearance()
        appearance.save()
        form.instance.appearance = appearance
        room = form.save()
        room_administrator = models.RoomAdministrator()
        room_administrator.room = room
        room_administrator.administrator = room.created_by
        room_administrator.save()
        messages.success(self.request, "Your room has been created")
        return HttpResponseRedirect(self.get_success_url(room))

    def get_success_url(self, room):
        return "{0}?room={1}".format(reverse('dashboard_general'), room.id)
