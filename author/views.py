from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from author.forms import UploadTaskForm
from author.utils import process_uploaded_task
from author.models import UploadedTask


class PanelView(TemplateView):

    template_name = 'author/panel.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PanelView, self).get_context_data(*args, **kwargs)
        context['form'] = UploadTaskForm()
        context['uploaded_tasks'] = UploadedTask.objects.filter(
            author=self.request.user
        )
        return context

    def post(self, req):
        form = UploadTaskForm(req.POST, req.FILES)
        if not form.is_valid():
            context = RequestContext(req, {'form': form})
            return render_to_response(self.template_name,
                                      context_instance=context)

        uploaded_file = req.FILES['task_file']
        process_uploaded_task(uploaded_file, req.user)

        return redirect('panel')
