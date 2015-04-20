from django.conf.urls import patterns, include, url
from django.contrib import admin

from slr1.views import IndexView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'slr1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
