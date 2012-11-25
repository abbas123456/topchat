from django.conf.urls import patterns, url
from client.views import ChatPageView, PrivateConversationView, StandaloneChatPageView, \
                         RoomApiView
from account.views import UserCreateView, UserDetailView, \
                          UserApiView, UserPasswordApiView, UserListCreateApiView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^$', ChatPageView.as_view(), {'pk': 1}, name='home'),
    url(r'^room/(?P<slug>[-\w\d]+)/(?P<pk>\d+)/$',
        ChatPageView.as_view(), name='room_detail'),
    url(r'^private-conversation/[^\s-]+/$',
        PrivateConversationView.as_view(), name='private_conversation'),
    url(r'^standalone-room/(?P<pk>\d+)/$',
        StandaloneChatPageView.as_view(), name='standalone_room_detail'),
    url(r'^room/(?P<pk>\d+)/$', RoomApiView.as_view(), name='room-detail'),
    url(r'^accounts/register/$', UserCreateView.as_view(), name='register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        name='login'),
    url(r'^accounts/profile/$', UserDetailView.as_view(), name='profile'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        name='logout'),
    url(r'^user/(?P<username>[-\w\d]+)/$', UserApiView.as_view(),
        name='user-detail'),
    url(r'^user/(?P<username>[-\w\d]+)/(?P<password>[-\w\d]+)/$',
        UserPasswordApiView.as_view(), name='user-password-detail'),
    url(r'^users/$',
        UserListCreateApiView.as_view(), name='users'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
