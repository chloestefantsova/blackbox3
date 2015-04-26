from tempfile import mkstemp
from os import rename
from os import path
from os import fdopen
from os.path import splitext
from hashlib import sha1

from django.conf import settings

from author.models import UploadedTask
from author.models import TaskUploadProgress


def process_uploaded_task(uploaded_file, author):

    uploaded_task = UploadedTask(author=author)
    uploaded_task.save()

    progress0 = TaskUploadProgress(uploaded_task=uploaded_task,
                                   progress=0)
    progress0.save()

    f_fd, f_path = mkstemp(dir=settings.UPLOADED_TASK_DIR)
    f_file = fdopen(f_fd, 'wb')
    sha1obj = sha1()
    for chunk in uploaded_file.chunks():
        f_file.write(chunk)
        sha1obj.update(chunk)
    f_file.close()
    sha1val = sha1obj.hexdigest()
    _, old_ext = splitext(uploaded_file.name)
    new_name = '%s%s' % (sha1val, old_ext)
    new_path = path.join(settings.UPLOADED_TASK_DIR, new_name)
    rename(f_path, new_path)

    progress100 = TaskUploadProgress(uploaded_task=uploaded_task,
                                     progress=100)
    progress100.save()

    uploaded_task.path = new_path
    uploaded_task.save()
