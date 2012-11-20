from django.conf.urls import patterns, url
from client.views import ChatPageView, RoomList
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^$', ChatPageView.as_view(), {'pk': 1}, name='home'),
    url(r'^room/(?P<slug>[-\w\d]+)/(?P<pk>\d+)/$',
        ChatPageView.as_view(), name='room_detail'),
    url(r'^rooms/$', RoomList.as_view(), name='room-list'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
