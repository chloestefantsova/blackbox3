from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from author.utils import process_uploaded_task
from author.models import UploadedTask
from author.models import TaskUploadProgress
from reg.models import Team, Member
from api.serializers import TeamSerializer
from api.serializers import MemberSerializer
from api.serializers import TaskUploadProgressSerializer


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


class TaskUploadAPIView(APIView):

    parser_classes = (FileUploadParser,)

    def put(self, req, filename=None, format=None):
        file_obj = req.data['file']
        uploaded_task = UploadedTask.objects.get(
            pk=req.QUERY_PARAMS.get('uploaded_task_pk')
        )
        process_uploaded_task(file_obj, uploaded_task)
        return Response(status=HTTP_201_CREATED)


class TaskUploadStartAPIView(APIView):

    def post(self, req, *args, **kwargs):
        uploaded_task = UploadedTask(author=self.request.user)
        uploaded_task.save()
        return Response({'uploaded_task_pk': uploaded_task.pk},
                        status=HTTP_201_CREATED)


class TaskUploadProgressAPIView(ListAPIView):

    serializer_class = TaskUploadProgressSerializer

    def get_queryset(self):
        queryset = TaskUploadProgress.objects.all()
        uploaded_task_pk = self.request.QUERY_PARAMS.get('uploaded_task_pk')
        if uploaded_task_pk is not None:
            queryset = queryset.filter(uploaded_task__pk=uploaded_task_pk)
        return queryset.order_by('-progress')
