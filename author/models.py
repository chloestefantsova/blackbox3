from os import path

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class UploadedTask(models.Model):

    author = models.ForeignKey(User)
    task = models.ForeignKey('game.Task', null=True, blank=True)
    path = models.CharField(null=False, blank=True, max_length=1024)
    format_checks_passed = models.BooleanField(default=False)
    untarred_path = models.CharField(null=False, blank=True, max_length=1024)
    created_at = models.DateTimeField(null=False, blank=True)

    def get_filename(self):
        return path.basename(self.path)

    def is_installed(self):
        return self.task is not None and self.task

    def is_failed(self):
        return TaskUploadProgress.objects.filter(
            uploaded_task=self,
            progress=TaskUploadProgress.PROGRESS_FAILED,
        ).exists()

    def is_uploaded(self):
        return TaskUploadProgress.objects.filter(
            uploaded_task=self,
            progress=100,
        ).exists()

    def is_correct(self):
        return self.format_checks_passed

    def is_untarred(self):
        return bool(self.untarred_path)

    def has_docker_images(self):
        return self.images.all().exists()

    def files_are_deployed(self):
        for file in self.files.all():
            if not file.is_deployed():
                return False
        for image in self.images.all():
            if not image.is_deployed():
                return False
        return True

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.created_at = timezone.now()
        return super(UploadedTask, self).save(*args, **kwargs)


class UploadedTaskFile(models.Model):

    uploaded_task = models.ForeignKey('author.UploadedTask',
                                      related_name='files',
                                      null=False,
                                      blank=False)

    untarred_path = models.CharField(null=False, blank=True, max_length=1024)
    relative_path = models.CharField(null=False, blank=True, max_length=1024)

    def is_deployed(self):
        return bool(self.relative_path)

    def get_link(self):
        return '%s%s' % (settings.UPLOADED_FILES_URL, self.relative_path)

    def get_full_path(self):
        return path.join(settings.UPLOADED_FILES_DIR, self.relative_path)


class UploadedTaskImage(models.Model):

    uploaded_task = models.ForeignKey('author.UploadedTask',
                                      related_name='images',
                                      null=False,
                                      blank=False)

    tcp_ports_str = models.CharField(null=False, blank=True, max_length=1024)
    udp_ports_str = models.CharField(null=False, blank=True, max_length=1024)

    untarred_path = models.CharField(null=False, blank=True, max_length=1024)
    relative_path = models.CharField(null=False, blank=False, max_length=1024)

    def is_deployed(self):
        return bool(self.relative_path)

    def get_link(self):
        return '%s%s' % (settings.UPLOADED_IMAGES_URL, self.relative_path)

    def get_full_path(self):
        return path.join(settings.UPLOADED_IMAGES_DIR, self.relative_path)


class UploadedTaskDeployStatus(models.Model):

    PHASE_FORMAT_CHECK = 'FC'
    PHASE_UNTAR = 'UT'
    PHASE_MOVE_FILES = 'MV'
    PHASE_EMAIL_DEPLOYERS = 'EM'
    PHASE_MAKE_TASK = 'MT'

    PHASE_CHOICES = (
        (PHASE_FORMAT_CHECK, 'format check'),
        (PHASE_UNTAR, 'untar'),
        (PHASE_MOVE_FILES, 'move files'),
        (PHASE_EMAIL_DEPLOYERS, 'email docker deployers'),
        (PHASE_MAKE_TASK, 'make task'),
    )

    uploaded_task = models.ForeignKey('author.UploadedTask',
                                      related_name='status',
                                      null=False,
                                      blank=False)
    phase = models.CharField(max_length=2, null=False, blank=True,
                             choices=PHASE_CHOICES)
    message = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.timestamp = timezone.now()
        return super(UploadedTaskDeployStatus, self).save(*args, **kwargs)


class TaskUploadProgress(models.Model):

    PROGRESS_FAILED = -1

    uploaded_task = models.ForeignKey('author.UploadedTask',
                                      related_name='progress',
                                      null=False,
                                      blank=False)

    progress = models.IntegerField(null=False, blank=False)

    timestamp = models.DateTimeField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.timestamp = timezone.now()
        return super(TaskUploadProgress, self).save(*args, **kwargs)
