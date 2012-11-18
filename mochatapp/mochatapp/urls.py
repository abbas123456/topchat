from django.conf.urls import patterns, url
from client.views import ChatPageView

urlpatterns = patterns('',
    url(r'^$', ChatPageView.as_view(), name='home'),
)
