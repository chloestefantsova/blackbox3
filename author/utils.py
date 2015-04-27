from os import path
from os.path import splitext
from hashlib import sha1
from io import BytesIO

from django.conf import settings
from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.uploadhandler import StopFutureHandlers
from django.core.files.uploadedfile import InMemoryUploadedFile

from author.models import UploadedTask
from author.models import TaskUploadProgress


class TaskUploadHandler(FileUploadHandler):

    def __init__(self, *args, **kwargs):
        super(TaskUploadHandler, self).__init__(*args, **kwargs)
        self.bytes_passed = 0
        self.uploaded_task = UploadedTask(author=self.request.user)
        self.uploaded_task.save()
        self.file = None
        self.sha1 = sha1()

    def receive_data_chunk(self, raw_data, start):
        self.bytes_passed += len(raw_data)
        percent = self.bytes_passed * 100 / self.content_length
        progress = TaskUploadProgress(uploaded_task=self.uploaded_task,
                                      progress=percent)
        progress.save()
        self.file.write(raw_data)
        self.sha1.update(raw_data)
        return raw_data

    def file_complete(self, file_size):
        if not TaskUploadProgress.objects.filter(
                uploaded_task=self.uploaded_task,
                progress=100).exists():
            progress100 = TaskUploadProgress(uploaded_task=self.uploaded_task,
                                             progress=100)
            progress100.save()
        _, ext = splitext(self.file_name)
        new_name = '%s%s' % (self.sha1.hexdigest(), ext)
        new_path = path.join(settings.UPLOADED_TASK_DIR, new_name)
        self.uploaded_task.path = new_path
        self.uploaded_task.save()
        self.file.seek(0)
        return InMemoryUploadedFile(
            file=self.file,
            field_name=self.field_name,
            name=new_name,
            content_type=self.content_type,
            size=file_size,
            charset=self.charset,
            content_type_extra=self.content_type_extra,
        )

    def new_file(self, *args, **kwargs):
        super(TaskUploadHandler, self).new_file(*args, **kwargs)
        progress0 = TaskUploadProgress(uploaded_task=self.uploaded_task,
                                       progress=0)
        progress0.save()
        self.file = BytesIO()
        raise StopFutureHandlers()


def process_uploaded_task(uploaded_file):
    filename = path.join(settings.UPLOADED_TASK_DIR, uploaded_file.name)
    f_file = file(filename, 'wb')
    for chunk in uploaded_file.chunks():
        f_file.write(chunk)
    f_file.close()
