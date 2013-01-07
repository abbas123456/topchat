from django.views import generic
from core.client import models
from core.client.forms import RoomSearchForm
from rest_framework import generics
from core.client.serializers import RoomSerializer, BannedUserSerializer
from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from django.conf import settings


class ChatPageView(generic.DetailView):
    model = models.Room

    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)
        context['websocket_string'] = settings.WEBSOCKET_STRING
        return context

class StandaloneChatPageView(ChatPageView):
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

class RoomSearchView(FacetedSearchView):

    def __init__(self, *args, **kwargs):
        sqs = SearchQuerySet().order_by('name').facet('category')
        FacetedSearchView.__init__(self, searchqueryset=sqs, form_class=RoomSearchForm)


    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
        extra['request'] = self.request
        facet_counts = self.results.facet_counts()
        facet_counts['fields'].update({'category':sorted(facet_counts['fields']['category'])})
        extra['facets']  = facet_counts
        return extra

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