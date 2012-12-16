from django.conf.urls import patterns, url
from client import views as client_views
from topchat.views import HomePageView, AboutPageView, GetStartedPageView, \
    HoldingPageView
from account.views import UserCreateView, UserDetailView, \
    UserApiView, UserPasswordApiView, \
    UserListCreateApiView
from dashboard import views as dashboard_views

from rest_framework.urlpatterns import format_suffix_patterns
from topchat.sitemap import StaticSitemap
from django.contrib.auth.decorators import login_required

sitemaps = {
    'main': StaticSitemap,
}

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^room/(?P<slug>[-\w\d]+)/(?P<pk>\d+)/$',
        client_views.ChatPageView.as_view(), name='room_detail'),
    url(r'^private-conversation/(?P<username>[^\s-]+)/$',
        client_views.PrivateConversationView.as_view(),
        name='private_conversation'),
    url(r'^standalone-room/(?P<pk>\d+)/$',
        client_views.StandaloneChatPageView.as_view(),
        name='standalone_room_detail'),
    url(r'^create-room/$',
        login_required(client_views.CreateRoomView.as_view()),
        name='create_room'),
    # Dashboard
    url(r'^dashboard/',
        login_required(dashboard_views.GeneralPageView.as_view()),
        name='dashboard_general'),
    url(r'^appearance/',
        login_required(dashboard_views.AppearancePageView.as_view()),
        name='dashboard_appearance'),
    url(r'^administrators/',
        login_required(dashboard_views.AdministratorsPageView.as_view()),
        name='dashboard_administrators'),
    # Static
    url(r'^about/$', AboutPageView.as_view(), name='about'),
    url(r'^get-started/$', GetStartedPageView.as_view(), name='get_started'),
    url(r'^holding/$', HoldingPageView.as_view(), name='holding'),

    # Authentication
    url(r'^accounts/register/$', UserCreateView.as_view(), name='register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        name='login'),
    url(r'^accounts/profile/$', UserDetailView.as_view(), name='profile'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        name='logout'),

    # REST api
    url(r'^room/(?P<pk>\d+)/$', client_views.RoomApiView.as_view(),
        name='room-detail'),
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
