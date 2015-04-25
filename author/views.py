from django.views.generic.base import TemplateView


class PanelView(TemplateView):

    template_name = 'author/panel.html'
