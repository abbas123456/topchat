from django.views import generic
from core.client import models
from rest_framework import generics
from core.client.serializers import RoomSerializer, BannedUserSerializer


class ChatPageView(generic.DetailView):
    model = models.Room

    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)
        context['rooms'] = models.Room.objects.all()
        return context


class StandaloneChatPageView(generic.DetailView):
    model = models.Room
    template_name = 'client/standalone_room_detail.html'


class PrivateConversationView(generic.DetailView):
    template_name = 'client/private_conversation.html'
    model = models.Room

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
    model = models.Room
    serializer_class = RoomSerializer


class BanUserApiView(generics.ListCreateAPIView):
    queryset = models.RoomBannedUser.objects.all()
    serializer_class = BannedUserSerializer