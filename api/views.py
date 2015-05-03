from django.db.models import Prefetch
from django.db.models import Q
from django.core.cache import cache

from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_200_OK

from author.utils import process_uploaded_task
from author.models import UploadedTask
from author.models import TaskUploadProgress
from author.models import UploadedTaskDeployStatus
from author.tasks import deploy_uploaded_task
from reg.models import Team, Member
from game.models import Task
from game.models import Answer
from game.tasks import recalc_data
from api.serializers import TeamSerializer
from api.serializers import MemberSerializer
from api.serializers import TaskUploadProgressSerializer
from api.serializers import UploadedTaskSerializer
from api.serializers import UploadedTaskDeployStatusSerializer
from api.serializers import TaskSerializer


class TeamAPIView(ListModelMixin,
                  CreateModelMixin,
                  GenericAPIView):

    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        return queryset.exclude(is_hidden=True)

    def get(self, req, *args, **kwargs):
        return self.list(req, *args, **kwargs)

    def post(self, req, *args, **kwargs):
        return self.create(req, *args, **kwargs)


class MemberAPIView(CreateModelMixin,
                    GenericAPIView):

    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def post(self, req, *args, **kwargs):
        return self.create(req, *args, **kwargs)


# TODO: only for authors
class TaskUploadAPIView(APIView):

    parser_classes = (FileUploadParser,)

    def put(self, req, filename=None, format=None):
        file_obj = req.data['file']
        uploaded_task = UploadedTask.objects.get(
            pk=req.QUERY_PARAMS.get('uploaded_task_pk')
        )
        process_uploaded_task(file_obj, uploaded_task)
        deploy_uploaded_task.delay(uploaded_task)
        return Response({}, status=HTTP_201_CREATED)


# TODO: only for the author who initiated upload
class TaskUploadStartAPIView(APIView):

    def post(self, req, *args, **kwargs):
        uploaded_task = UploadedTask(author=self.request.user)
        uploaded_task.save()
        return Response({'uploaded_task_pk': uploaded_task.pk},
                        status=HTTP_201_CREATED)


# TODO: only for author of the task
class TaskUploadProgressAPIView(ListAPIView):

    serializer_class = TaskUploadProgressSerializer

    def get_queryset(self):
        queryset = TaskUploadProgress.objects.all()
        uploaded_task_pk = self.request.QUERY_PARAMS.get('uploaded_task_pk')
        if uploaded_task_pk is not None:
            queryset = queryset.filter(uploaded_task__pk=uploaded_task_pk)
        return queryset.order_by('-progress')


# TODO: only for author of the tasks
class UploadedTaskAPIView(ListAPIView):

    serializer_class = UploadedTaskSerializer

    def get_queryset(self):
        queryset = UploadedTask.objects.filter(
            Q(author=self.request.user) & ~Q(path='')
        )
        queryset = queryset.prefetch_related(Prefetch(
            'progress',
            queryset=TaskUploadProgress.objects.filter(progress=0),
            to_attr='progress0',
        ))
        queryset = queryset.prefetch_related(Prefetch(
            'progress',
            queryset=TaskUploadProgress.objects.filter(progress=100),
            to_attr='progress100',
        ))
        return queryset


# TODO: only for author of the tasks
class UploadedTaskDeployStatusAPIView(ListAPIView):

    serializer_class = UploadedTaskDeployStatusSerializer

    def get_queryset(self):
        return UploadedTaskDeployStatus.objects.filter(
            uploaded_task__pk=self.kwargs['uploaded_task_pk'],
        )


# TODO: only for author of the tasks
class AllUploadedTaskDeployStatusAPIView(ListAPIView):

    serializer_class = UploadedTaskDeployStatusSerializer

    def get_queryset(self):
        return UploadedTaskDeployStatus.objects.filter(
            uploaded_task__author=self.request.user
        )


class TaskListAPIView(ListAPIView):

    serializer_class = TaskSerializer

    def get_queryset(self):
        selected_pks = cache.get('published')
        if selected_pks is None:
            queryset = Task.objects.all()
            selected_pks = [task.pk for task in queryset if task.is_published()]
        return Task.objects.filter(pk__in=selected_pks)


class SolvedTaskAPIView(ListAPIView):

    serializer_class = TaskSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'member'):
            team_pk = self.request.user.member.team.pk
            result = cache.get('solved%d' % team_pk)
            if result is None:
                result = []
            return Task.objects.filter(pk__in=result)
        return Task.objects.filter(pk=-1)


class FlagAPIView(APIView):

    def post(self, req, *args, **kwargs):
        task_pk = req.POST.get('task')
        flag = req.POST.get('flag')

        tasks = Task.objects.filter(pk=task_pk)
        if not tasks:
            return Response({'error': 'No such task.'},
                            status=HTTP_400_BAD_REQUEST)
        task = tasks[0]
        Answer(task=task, member=req.user.member, flag=flag).save()
        if task.check_answer(flag):
            recalc_data.delay(req.user.member.team.pk)
            return Response({'result': 'Congrats!'},
                            status=HTTP_200_OK)

        return Response({'result': 'Wrong flag.'},
                        status=HTTP_200_OK)


class MeAPIView(APIView):

    def get(self, req, *args, **kwargs):
        resp = {}

        if hasattr(req, 'user') and req.user.is_authenticated():
            resp = {'username': req.user.username}
            if hasattr(req.user, 'member'):
                resp['team'] = req.user.member.team.name
            else:
                resp['team'] = ''

        return Response(resp, status=HTTP_200_OK)


class RatingAPIView(APIView):

    def get(self, req, *args, **kwargs):
        result = cache.get('rating')
        if result is None:
            result = []
        return Response(result, status=HTTP_200_OK)
