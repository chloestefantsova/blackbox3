from django.conf.urls import patterns, url

from api.views import TeamAPIView
from api.views import MemberAPIView
from api.views import TaskUploadAPIView


urlpatterns = patterns(
    '',

    url(r'^teams/$', TeamAPIView.as_view(), name='teams'),
    url(r'^members/$', MemberAPIView.as_view(), name='members'),
    url(r'^upload/$', TaskUploadAPIView.as_view(), name='api-upload'),
)
