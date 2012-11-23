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
        
class RoomApiView(generics.RetrieveAPIView):
    model = Room
    serializer_class = RoomSerializer
