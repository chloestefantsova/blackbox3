from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from author.utils import process_uploaded_task
from reg.models import Team, Member
from api.serializers import TeamSerializer
from api.serializers import MemberSerializer


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
        process_uploaded_task(file_obj, req.user)
        return Response(status=HTTP_201_CREATED)
