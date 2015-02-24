from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from gps import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'automon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.appDefault, name='appDefault'),
    url(r'^gps/', include('gps.urls', namespace='gps')),
    url(r'^admin/', include(admin.site.urls)),
)
