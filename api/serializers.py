from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, ValidationError, RelatedField, HiddenField, CharField, Field

from reg.models import Team, Member


class TeamSerializer(ModelSerializer):

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
        exclude = ('auth_string',)
        read_only_fields = ('id', 'created_at')


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
            raise ValidationError(_('Entered password values do not match.'))
        return data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')


class TeamField(RelatedField):

    def to_internal_value(self, data):
        return Team.objects.get(auth_string=data)

    def to_representation(self, value):
        return value.name


class MemberSerializer(ModelSerializer):

    user = UserSerializer()
    team = TeamField(queryset=Team.objects.all())

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
        read_only_fields = ('id', 'created_at')
