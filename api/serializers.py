from datetime import datetime
from time import mktime

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from rest_framework.serializers import RelatedField
from rest_framework.serializers import CharField
from rest_framework.serializers import Field
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import SerializerMethodField

from reg.models import Team
from reg.models import Member
from author.models import TaskUploadProgress
from author.models import UploadedTask
from author.models import UploadedTaskDeployStatus
from game.models import Task


class UnixEpochDateTimeField(DateTimeField):

    def to_internal_value(self, data):
        return datetime.fromtimestamp(float(data))

    def to_representation(self, value):
        return int(mktime(value.timetuple()))


class EmptyCountryField(CharField):

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        if not value:
            return u''
        return unicode(value.name)


class TeamSerializer(ModelSerializer):

    created_at = UnixEpochDateTimeField(read_only=True)
    flag = SerializerMethodField()
    country = EmptyCountryField()

    def get_flag(self, obj):
        return obj.country.flag

    def validate(self, data):
        error_dict = {}
        if 'is_school' in data and data['is_school']:
            if 'school_name' not in data or not data['school_name'].strip():
                error_dict['school_name'] = [_('The field is required for school teams')]
            if 'teacher_name' not in data or not data['teacher_name'].strip():
                error_dict['teacher_name'] = [_('The field is required for school teams')]
            if 'teacher_email' not in data or not data['teacher_email'].strip():
                error_dict['teacher_email'] = [_('The field is required for school teams')]
            if 'address' not in data or not data['address'].strip():
                error_dict['address'] = [_('The field is required for school teams')]
        if len(error_dict) > 0:
            raise ValidationError(error_dict)
        return data

    class Meta:
        model = Team
        exclude = ('id', 'auth_string',)
        read_only_fields = ('created_at',)
        write_only_fields = ('teacher_name', 'teacher_email', 'leader_email', 'address')


class PasswordField(Field):

    def to_representation(self, obj):
        return ''

    def to_internal_value(self, data):
        return data


class UserSerializer(ModelSerializer):

    password1 = PasswordField(write_only=True)
    password2 = PasswordField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            error_msg = _('Entered password values do not match.')
            raise ValidationError({'password1': [error_msg],
                                   'password2': [error_msg]})
        return data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')


class TeamField(RelatedField):

    def to_internal_value(self, data):
        teams = Team.objects.filter(auth_string=data)
        if teams.exists():
            return teams[0]
        return None

    def to_representation(self, value):
        return value.name


class MemberSerializer(ModelSerializer):

    user = UserSerializer()
    team = TeamField(queryset=Team.objects.all())

    def validate_team(self, value):
        if value is None:
            raise ValidationError(_('Authentication string is unknown or is incorrectly entered.'))
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data['password1']
        del user_data['password1']
        del user_data['password2']
        user = User(**user_data)
        user.set_password(password)
        user.save()
        validated_data['user'] = user
        member = Member(**validated_data)
        member.save()
        return member

    class Meta:
        model = Member
        fields = ('pk', 'created_at', 'user', 'team')
        read_only_fields = ('pk', 'created_at')


class TaskUploadProgressSerializer(ModelSerializer):

    timestamp = UnixEpochDateTimeField(read_only=True)

    class Meta:
        model = TaskUploadProgress
        fields = ('progress', 'timestamp')
        read_only_fields = ('progress', 'timestamp')


class UploadedTaskSerializer(ModelSerializer):

    upload_begin_timestamp = SerializerMethodField()
    upload_end_timestamp = SerializerMethodField()
    filename = SerializerMethodField()
    created_at = UnixEpochDateTimeField(read_only=True)

    def get_upload_begin_timestamp(self, obj):
        if obj.progress0:
            timestamp = obj.progress0[0].timestamp
            return int(mktime(timestamp.timetuple()))
        return -1

    def get_upload_end_timestamp(self, obj):
        if obj.progress100:
            timestamp = obj.progress100[0].timestamp
            return int(mktime(timestamp.timetuple()))
        return -1

    def get_filename(self, obj):
        return obj.get_filename()

    class Meta:
        model = UploadedTask
        fields = ('pk', 'author', 'task', 'created_at', 'filename',
                  'upload_begin_timestamp', 'upload_end_timestamp')
        read_only_fields = ('pk', 'author', 'task', 'created_at')


class UploadedTaskDeployStatusSerializer(ModelSerializer):

    phase = SerializerMethodField()
    timestamp = UnixEpochDateTimeField(read_only=True)

    def get_phase(self, obj):
        return dict(UploadedTaskDeployStatus.PHASE_CHOICES)[obj.phase]

    class Meta:
        model = UploadedTaskDeployStatus
        fields = ('pk', 'uploaded_task', 'phase', 'message', 'timestamp')
        read_only_fields = ('pk', 'uploaded_task', 'phase', 'message',
                            'timestamp')


class TaskSerializer(ModelSerializer):

    title = SerializerMethodField()
    desc = SerializerMethodField()

    def get_title(self, obj):
        return obj.get_title()

    def get_desc(self, obj):
        return obj.get_desc()

    class Meta:
        model = Task
        fields = ('pk', 'title', 'category', 'cost', 'desc')
        read_only_fields = ('pk', 'title', 'category', 'cost', 'desc')
