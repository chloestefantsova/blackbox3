from django.db.models import Prefetch
from django.db.models import Q
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import ugettext as _

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
from api.serializers import TeamListSerializer
from api.serializers import TeamCreateSerializer
from api.serializers import MemberSerializer
from api.serializers import TaskUploadProgressSerializer
from api.serializers import UploadedTaskSerializer
from api.serializers import UploadedTaskDeployStatusSerializer
from api.serializers import TaskSerializer


class TeamAPIView(ListModelMixin,
                  CreateModelMixin,
                  GenericAPIView):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeamCreateSerializer
        return TeamListSerializer

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
        selected = cache.get('published')
        if selected is None:
            queryset = Task.objects.all()
            published_pks = [task.pk for task in queryset if task.is_published()]
            queryset = Task.objects.filter(pk__in=published_pks)
            cache.set('published', queryset, timeout=None)
            return queryset
        return selected


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
            return Response({'error': _('No such task.')},
                            status=HTTP_400_BAD_REQUEST)
        task = tasks[0]

        game = task.get_game()
        if game is None or game.ends_at <= timezone.now():
            return Respone({'result': _('Game over!')},
                           status=HTTP_400_BAD_REQUEST)

        Answer(task=task, member=req.user.member, flag=flag).save()
        if task.check_answer(flag):
            recalc_data.delay(req.user.member.team.pk)
            return Response({'result': _('Congrats!')},
                            status=HTTP_200_OK)

        return Response({'result': _('Wrong flag.')},
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


class StandingsAPIView(APIView):

    def get(self, req, *args, **kwargs):
        result = cache.get('rating')
        if result is None:
            result = []
        result.sort(lambda x, y: y['score'] - x['score'])
        standings = {'standings': []}
        pos = 0
        prev_score = -1
        for entry in result:
            if entry['score'] != prev_score:
                pos += 1
                prev_score = entry['score']
            standings_entry = {}
            standings_entry['team'] = entry['team_name']
            standings_entry['score'] = entry['score']
            standings_entry['pos'] = pos
            standings['standings'].append(standings_entry)
        return Response(standings, status=HTTP_200_OK)
