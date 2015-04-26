from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UploadedTask(models.Model):

    author = models.ForeignKey(User)
    task = models.ForeignKey('game.Task', null=True, blank=True)
    path = models.CharField(null=False, blank=True, max_length=1024)

    def is_installed(self):
        return self.task is not None and self.task

    def is_failed(self):
        return TaskUploadProgress.objects.filter(
            uploaded_task=self,
            progress=TaskUploadProgress.PROGRESS_FAILED,
        ).exists()

    def is_uploaded(self):
        return TaskUploadProgress.objects.filter(
            upload_task=self,
            progress=100,
        ).exists()


class TaskUploadProgress(models.Model):

    PROGRESS_FAILED = -1

    uploaded_task = models.ForeignKey('author.UploadedTask',
                                      null=False,
                                      blank=False)

    progress = models.IntegerField(null=False, blank=False)

    timestamp = models.DateTimeField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.timestamp = timezone.now()
        return super(TaskUploadProgress, self).save(*args, **kwargs)
