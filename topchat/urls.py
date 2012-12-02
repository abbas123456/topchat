from django.conf.urls import patterns, url
from client.views import ChatPageView, PrivateConversationView, StandaloneChatPageView, \
                         RoomApiView
from topchat.views import HomePageView, AboutPageView, GettingStartedPageView, HoldingPageView                        
from account.views import UserCreateView, UserDetailView, \
                          UserApiView, UserPasswordApiView, UserListCreateApiView
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from topchat.sitemap import StaticSitemap

sitemaps = {
    'main': StaticSitemap,
}

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^room/(?P<slug>[-\w\d]+)/(?P<pk>\d+)/$',
        ChatPageView.as_view(), name='room_detail'),
    url(r'^private-conversation/(?P<username>[^\s-]+)/$',
        PrivateConversationView.as_view(), name='private_conversation'),
    url(r'^standalone-room/(?P<pk>\d+)/$',
        StandaloneChatPageView.as_view(), name='standalone_room_detail'),
    url(r'^about/$', AboutPageView.as_view(), name='about'),
    url(r'^getting-started/$', GettingStartedPageView.as_view(), name='getting_started'),
    url(r'^holding/$', HoldingPageView.as_view(), name='holding'),
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
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
