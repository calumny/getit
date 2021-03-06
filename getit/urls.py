from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'getit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/', include('api.urls', namespace="api")),
    url(r'^map/', include('map.urls', namespace="map")),
    url(r'^launch/', include('launch.urls', namespace="launch")),
    url(r'^$', include('map.urls', namespace="map")),
)
