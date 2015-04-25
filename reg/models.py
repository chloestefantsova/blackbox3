import string
import random

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.conf import settings

from django_countries.fields import CountryField


class Team(models.Model):
    name = models.CharField(max_length=256, unique=True, blank=False)
    is_school = models.BooleanField(null=False, blank=False, default=False)
    school_name = models.CharField(max_length=1024, null=False, blank=True)
    country = CountryField(null=False, blank=True)
    teacher_name = models.CharField(max_length=256, null=False, blank=True)
    teacher_email = models.EmailField(null=True, blank=True)
    leader_email = models.EmailField(null=False, blank=False)
    address = models.TextField(null=False, blank=True)
    auth_string = models.CharField(max_length=32, null=False, blank=True)
    created_at = models.DateTimeField(null=False, blank=True)
    is_hidden = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            alphabet = string.lowercase + string.digits
            random_letters = [random.choice(alphabet) for _ in xrange(32)]
            self.auth_string = ''.join(random_letters)
            self.created_at = timezone.now()
        return super(Team, self).save(*args, **kwargs)


class Member(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team)
    created_at = models.DateTimeField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created_at = timezone.now()
        return super(Member, self).save(*args, **kwargs)


def welcome_team(sender, instance, **kwargs):
    if kwargs['created']:
        recipients = [instance.leader_email]
        if instance.teacher_email:
            recipients.append(instance.teacher_email)
        subject_template = _('Welcome to School CTF Spring 2015, {team_name}!')
        send_mail(subject_template.format(team_name=instance.name),
                  render_to_string('welcome-team-email.txt',
                                   {'auth_string': instance.auth_string}),
                  'School CTF Jury <%s>' % settings.EMAIL_HOST_USER,
                  recipients,
                  fail_silently=True)

post_save.connect(welcome_team, sender=Team)


def welcome_participant(sender, instance, **kwargs):
    if kwargs['created']:
        recipients = [instance.team.leader_email]
        if instance.team.teacher_email:
            recipients.append(instance.team.teacher_email)
        subject_template = _('Participant {full_name} joined team {team_name}')
        send_mail(subject_template.format(full_name=instance.user.first_name,
                                          team_name=instance.team.name),
                  render_to_string('welcome-participant-email.txt',
                                   {'full_name': instance.user.first_name,
                                    'team_name': instance.team.name}),
                  'School CTF Jury <%s>' % settings.EMAIL_HOST_USER,
                  recipients,
                  fail_silently=True)

post_save.connect(welcome_participant, sender=Member)
