from django.conf.urls import patterns, url

from api.views import TeamAPIView, MemberAPIView


urlpatterns = patterns('',
    url(r'^teams/$', TeamAPIView.as_view(), name='teams'),
    url(r'^members/$', MemberAPIView.as_view(), name='members'),
)
