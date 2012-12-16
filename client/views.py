from django.views import generic
from client.models import Room
from rest_framework import generics
from client.serializers import RoomSerializer
from client import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages


class ChatPageView(generic.DetailView):
    model = Room

    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        return context


class StandaloneChatPageView(generic.DetailView):
    model = Room
    template_name = 'client/standalone_room_detail.html'


class PrivateConversationView(generic.TemplateView):
    template_name = 'client/private_conversation.html'

    def get_context_data(self, **kwargs):
        context = super(PrivateConversationView, self).get_context_data(**kwargs)
        context['username'] = kwargs['username']
        return context


class RoomApiView(generics.RetrieveAPIView):
    model = Room
    serializer_class = RoomSerializer


class CreateRoomView(generic.CreateView):
    model = Room
    form_class = forms.RoomForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, "Your room has been created")
        return HttpResponseRedirect(self.get_success_url(form.instance))

    def get_success_url(self, room):
        return "{0}?room={1}".format(reverse('dashboard_general'), room.id)
