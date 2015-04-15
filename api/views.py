from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin

from reg.models import Team, Member
from api.serializers import TeamSerializer, MemberSerializer


class TeamAPIView(ListModelMixin,
                  CreateModelMixin,
                  GenericAPIView):

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

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
