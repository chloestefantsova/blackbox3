from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from api.views import TeamAPIView
from api.views import MemberAPIView
from api.views import TaskUploadAPIView
from api.views import TaskUploadStartAPIView
from api.views import TaskUploadProgressAPIView
from api.views import UploadedTaskAPIView
from api.views import UploadedTaskDeployStatusAPIView
from api.views import AllUploadedTaskDeployStatusAPIView
from api.views import TaskListAPIView
from api.views import FlagAPIView
from api.views import MeAPIView
from api.views import SolvedTaskAPIView
from api.views import RatingAPIView
from api.views import StandingsAPIView


urlpatterns = patterns(
    '',

    url(r'^me/$', MeAPIView.as_view(), name='me'),
    url(r'^teams/$', TeamAPIView.as_view(), name='teams'),
    url(r'^members/$', MemberAPIView.as_view(), name='members'),
    url(r'^upload/$', TaskUploadAPIView.as_view(), name='api-upload'),
    url(r'^upload/start/$', TaskUploadStartAPIView.as_view(),
        name='api-upload-start'),
    url(r'^upload/progress/', TaskUploadProgressAPIView.as_view(),
        name='api-upload-progress'),
    url(r'^upload/tasks/$', UploadedTaskAPIView.as_view(),
        name='api-uploaded-tasks'),
    url(r'^upload/tasks/(?P<uploaded_task_pk>\d+)/status/$',
        UploadedTaskDeployStatusAPIView.as_view(),
        name='api-uploaded-task-status'),
    url(r'^upload/tasks/status/$',
        AllUploadedTaskDeployStatusAPIView.as_view(),
        name='api-all-uploaded-task-status'),
    url(r'^tasks/$', TaskListAPIView.as_view(), name='api-tasks'),
    url(r'^tasks/solved/$',
        login_required(SolvedTaskAPIView.as_view()),
        name='api-tasks-solved'),
    url(r'^flag/$', login_required(FlagAPIView.as_view()), name='api-flag'),
    url(r'^rating/$', RatingAPIView.as_view(), name='api-rating'),
    url(r'^standings/$', StandingsAPIView.as_view(), name='api-rating'),
)
