from django.conf.urls import patterns, url

from api.views import TeamAPIView
from api.views import MemberAPIView
from api.views import TaskUploadAPIView
from api.views import TaskUploadStartAPIView
from api.views import TaskUploadProgressAPIView
from api.views import UploadedTaskAPIView


urlpatterns = patterns(
    '',

    url(r'^teams/$', TeamAPIView.as_view(), name='teams'),
    url(r'^members/$', MemberAPIView.as_view(), name='members'),
    url(r'^upload/$', TaskUploadAPIView.as_view(), name='api-upload'),
    url(r'^upload/start/$', TaskUploadStartAPIView.as_view(),
        name='api-upload-start'),
    url(r'^upload/progress/', TaskUploadProgressAPIView.as_view(),
        name='api-upload-progress'),
    url(r'^upload/tasks/$', UploadedTaskAPIView.as_view(),
        name='api-uploaded-tasks'),
)
