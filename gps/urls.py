from django.conf.urls import patterns, include, url
from gps import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'automon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.GpsNodesListView.as_view(), name='index'),
    url(r'add/$', views.GpsNodeCreate.as_view(), name='add'),
    url(r'delete/(?P<pk>\d+)/$', views.GpsNodeDelete.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/detail/$', views.GpsNodeDetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>\d+)/update/$', views.GpsNodeUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/update/$', views.GpsNodeUpdateView, name='update'),
)
