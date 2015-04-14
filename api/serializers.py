from django.utils.translation import ugettext as _

from rest_framework.serializers import ModelSerializer, ValidationError

from reg.models import Team


class TeamSerializer(ModelSerializer):

    def validate(self, data):
        if 'is_school' in data and data['is_school']:
            error_dict = {}
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
