import csv
import sys

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from django_countries import countries

from reg.models import Team


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--non-school',
            action='store_true',
            dest='non_school',
            default=False,
            help='Are we exporting school teams or non-school teams'),
        )

    def handle(self, *args, **options):
        is_school = not options['non_school']
        teams = Team.objects.filter(is_school=is_school)
        lines = []
        fields = ['name', 'country', 'members', 'school name', 'teacher', 'leader', 'address']
        for team in teams:
            team_line = {
                'name': team.name,
                'country': team.country,
                'school name': team.school_name,
                'teacher': '%s <%s>' % (team.teacher_name, team.teacher_email),
                'leader': team.leader_email,
                'address': team.address,
            }
            members = []
            for index, member in enumerate(team.member_set.all(), 1):
                if member.user.first_name:
                    member_line = u'(%d) %s a.k.a. %s' % (
                        index,
                        member.user.first_name,
                        member.user.username,
                    )
                else:
                    member_line = u'(%d) %s, real name is unknown' % (
                        index,
                        member.user.username,
                    )
                members.append(member_line)
            team_line['members'] = u', '.join(members)
            lines.append(team_line)

        for line in lines:
            for key in line:
                if key != 'country' or not line[key]:
                    line[key] = unicode(line[key]).encode('utf-8')
                else:
                    line[key] = unicode(countries.countries[line[key]])

        if not is_school:
            fields.remove('school name')
            fields.remove('teacher')
            for line in lines:
                del line['school name']
                del line['teacher']

        writer =  csv.DictWriter(sys.stdout, fieldnames=fields)
        writer.writeheader()
        for line in lines:
            try:
                writer.writerow(line)
            except Exception, ex:
                sys.stderr.write('%s, %s\n' % (line, ex))

        sys.stdout.flush()
