from django.views.generic import TemplateView, DetailView
from client.models import Room
from rest_framework import generics
from client.serializers import RoomSerializer

class ChatPageView(DetailView):
    model = Room
    
    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        return context

class StandaloneChatPageView(DetailView):
    model = Room
    template_name = 'client/standalone_room_detail.html'

class PrivateConversationView(TemplateView):
    template_name = 'client/private_conversation.html'
        
class RoomApiView(generics.RetrieveAPIView):
    model = Room
    serializer_class = RoomSerializer

