from django.conf.urls import patterns, url, include
from core.client import views as client_views
from core.topchat.views import HomePageView, AboutPageView, GetStartedPageView, \
    HoldingPageView
from core.account import views as account_views
from core.dashboard import views as dashboard_views

from rest_framework.urlpatterns import format_suffix_patterns
from core.topchat.sitemap import StaticSitemap
from django.contrib.auth.decorators import login_required
from haystack.views import FacetedSearchView

sitemaps = {
    'main': StaticSitemap,
}

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^room/(?P<slug>[-\w\d]+)/(?P<pk>\d+)/$',
        client_views.ChatPageView.as_view(), name='room_detail'),
    url(r'^private-conversation/(?P<pk>\d+)/(?P<username>[^\s-]+)/$',
        client_views.PrivateConversationView.as_view(),
        name='private_conversation'),
    url(r'^standalone-room/(?P<pk>\d+)/$',
        client_views.StandaloneChatPageView.as_view(),
        name='standalone_room_detail'),
    # Dashboard
    url(r'^create-room/$',
        login_required(dashboard_views.CreateRoomView.as_view()),
        name='create_room'),
    url(r'^dashboard/',
        login_required(dashboard_views.GeneralPageView.as_view()),
        name='dashboard_general'),
    url(r'^appearance/',
        login_required(dashboard_views.AppearancePageView.as_view()),
        name='dashboard_appearance'),
    url(r'^administrators/',
        login_required(dashboard_views.AdministratorsPageView.as_view()),
        name='dashboard_administrators'),
    url(r'^user-management/',
        login_required(dashboard_views.UserManagementPageView.as_view()),
        name='dashboard_user_management'),
    url(r'^your-website/',
        login_required(dashboard_views.YourWebsitePageView.as_view()),
        name='dashboard_your_website'),
    url(r'^delete-room/',
        login_required(dashboard_views.DeleteRoomView.as_view()),
        name='dashboard_delete_room'),
    # Static
    url(r'^about/$', AboutPageView.as_view(), name='about'),
    url(r'^get-started/$', GetStartedPageView.as_view(), name='get_started'),
    url(r'^holding/$', HoldingPageView.as_view(), name='holding'),

    # Authentication
    url(r'^accounts/register/$', account_views.UserCreateView.as_view(),
        name='register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        name='login'),
    url(r'^accounts/profile/$', account_views.UserDetailView.as_view(),
        name='profile'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        name='logout'),
    url(r'^accounts/generate-token/$', account_views.GenerateTokenView.as_view(),
        name='generate_token'),                   

    # REST api
    url(r'^rooms/(?P<pk>\d+)/$', client_views.RoomApiView.as_view()),
    url(r'^banned-users/$', client_views.BanUserApiView.as_view()),
    url(r'^user-tokens/(?P<token_string>[-\w\d]+)/$',
        account_views.UserAuthenticationTokenView.as_view()),
    url(r'^delete-user-token/(?P<token_string>[-\w\d]+)/$',
        account_views.UserAuthenticationTokenDeleteView.as_view()),
    url(r'^users/(?P<search_query>[-\w\d]+)/(?P<limit>\d+)/$',
        account_views.UserListApiView.as_view()),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    url(r'^search/', client_views.RoomSearchView()),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
