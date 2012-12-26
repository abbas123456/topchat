from django.views import generic
from client.models import Room
from rest_framework import generics
from client.serializers import RoomSerializer


class ChatPageView(generic.DetailView):
    model = Room

    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        return context


class StandaloneChatPageView(generic.DetailView):
    model = Room
    template_name = 'client/standalone_room_detail.html'


class PrivateConversationView(generic.DetailView):
    template_name = 'client/private_conversation.html'
    model = Room

    def get_context_data(self, **kwargs):
        context = super(PrivateConversationView, self).get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        context['room'] = self.get_object()
        return context


##############################################################################
##
## REST API VIEWS
##
##############################################################################


class RoomApiView(generics.RetrieveAPIView):
    model = Room
    serializer_class = RoomSerializer

