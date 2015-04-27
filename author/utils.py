from os import path
from os.path import splitext
from hashlib import sha1
from io import BytesIO
from re import match

from django.conf import settings
from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.uploadhandler import StopFutureHandlers
from django.core.files.uploadedfile import InMemoryUploadedFile

from author.models import UploadedTask
from author.models import TaskUploadProgress


def splitext_all(filename):
    result = ''
    filename, ext = splitext(filename)
    while ext:
        if len(ext) < 5 and not match(r'^\.\d+$', ext):
            result = ext + result
            filename, ext = splitext(filename)
        else:
            filename += ext
            ext = ''
    return filename, result


class TaskUploadHandler(FileUploadHandler):

    def __init__(self, *args, **kwargs):
        super(TaskUploadHandler, self).__init__(*args, **kwargs)
        self.bytes_passed = 0
        self.uploaded_task = UploadedTask.objects.get(
            pk=self.request.GET.get('uploaded_task_pk')
        )
        self.file = None
        self.sha1 = sha1()

    def receive_data_chunk(self, raw_data, start):
        self.bytes_passed += len(raw_data)
        percent = self.bytes_passed * 100 / self.content_length
        if not TaskUploadProgress.objects.filter(
                uploaded_task=self.uploaded_task,
                progress=percent).exists():
            progress = TaskUploadProgress(uploaded_task=self.uploaded_task,
                                          progress=percent)
            progress.save()
        self.file.write(raw_data)
        self.sha1.update(raw_data)

    def file_complete(self, file_size):
        if not TaskUploadProgress.objects.filter(
                uploaded_task=self.uploaded_task,
                progress=100).exists():
            progress100 = TaskUploadProgress(uploaded_task=self.uploaded_task,
                                             progress=100)
            progress100.save()
        file_name, ext = splitext_all(self.file_name)
        file_name = '%s%s' % (self.sha1.hexdigest(), ext)
        self.file.seek(0)
        return InMemoryUploadedFile(
            file=self.file,
            field_name=self.field_name,
            name=file_name,
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


def process_uploaded_task(uploaded_file, uploaded_task):
    full_name = path.join(settings.UPLOADED_TASK_DIR, uploaded_file.name)
    actual_file = file(full_name, 'wb')
    for chunk in uploaded_file.chunks():
        actual_file.write(chunk)
    actual_file.close()
    uploaded_task.path = full_name
    uploaded_task.save()
