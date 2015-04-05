from rest_framework.serializers import ModelSerializer

from reg.models import Team


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        exclude = ('auth_string',)
        read_only_fields = ('id', 'created_at')
