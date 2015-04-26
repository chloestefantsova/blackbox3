from tempfile import mkstemp
from os import rename
from os import path
from os import fdopen
from os.path import splitext
from hashlib import sha1

from django.views.generic.base import TemplateView
from django.views.generic import View
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext

from author.forms import UploadTaskForm
from author.models import UploadedTask
from author.models import TaskUploadProgress


class PanelView(TemplateView):

    template_name = 'author/panel.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PanelView, self).get_context_data(*args, **kwargs)
        context['form'] = UploadTaskForm()
        return context

    def post(self, req, *args, **kwargs):
        form = UploadTaskForm(req.POST, req.FILES)
        if not form.is_valid():
            context = RequestContext(req, {'form': form})
            return render_to_response(self.template_name,
                                      context_instance=context)

        uploaded_task = UploadedTask(author=req.user)
        uploaded_task.save()

        progress0 = TaskUploadProgress(uploaded_task=uploaded_task,
                                       progress=0)
        progress0.save()

        uploaded_file = req.FILES['task_file']
        f_fd, f_path = mkstemp(dir=settings.UPLOADED_TASK_DIR)
        f_file = fdopen(f_fd, 'wb')
        sha1obj = sha1()
        for chunk in uploaded_file.chunks():
            f_file.write(chunk)
            sha1obj.update(chunk)
        f_file.close()
        sha1val = sha1obj.hexdigest()
        old_name, old_ext = splitext(uploaded_file.name)
        new_name = '%s%s' % (sha1val, old_ext)
        new_path = path.join(settings.UPLOADED_TASK_DIR, new_name)
        rename(f_path, new_path)

        progress100 = TaskUploadProgress(uploaded_task=uploaded_task,
                                         progress=100)
        progress100.save()

        uploaded_task.path = new_path
        uploaded_task.save()

        return redirect('panel')
