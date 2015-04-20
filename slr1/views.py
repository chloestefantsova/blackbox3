from django.views.generic.base import TemplateView

from django_countries import countries


class IndexView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        country_list = list()
        for code, name in countries.countries.iteritems():
            country_list.append((code, unicode(name)))
        country_list.sort(lambda x, y: cmp(x[1], y[1]))
        context['countries'] = country_list
        return context
