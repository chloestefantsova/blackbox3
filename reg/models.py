import string
import random

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=256, unique=True, blank=False)
    is_school = models.BooleanField(null=False, blank=False, default=False)
    school_name = models.CharField(max_length=1024, null=False, blank=True)
    teacher_name = models.CharField(max_length=256, null=False, blank=True)
    teacher_email = models.EmailField(null=True, blank=True)
    leader_email = models.EmailField(null=False, blank=False)
    address = models.TextField(null=False, blank=True)
    auth_string = models.CharField(max_length=32, null=False, blank=True)
    created_at = models.DateTimeField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.auth_string = ''.join([random.choice(string.lowercase + string.digits) for i in xrange(32)])
            self.created_at = timezone.now()
        super(Team, self).save(*args, **kwargs)


class Member(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team)
    created_at = models.DateTimeField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created_at = timezone.now()
        super(Member, self).save(*args, **kwargs)
