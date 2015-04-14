from django.conf.urls import patterns, url

from api.views import TeamAPIView


urlpatterns = patterns('',
    url(r'^teams/$', TeamAPIView.as_view(), name='teams'),
)
