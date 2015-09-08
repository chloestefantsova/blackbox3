from django.views.generic.base import TemplateView
from django.utils.translation import ugettext as _

from django_countries import countries

from game.models import Game


class IndexView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        country_list = list()
        for code, name in countries.countries.iteritems():
            country_list.append((code, unicode(name)))
        country_list.sort(lambda x, y: cmp(x[1], y[1]))

        games = Game.objects.all()
        if len(games) != 1:
            game = None
            game_desc = _('The game is not set up')
        else:
            game = games[0]
            game_desc = game.get_desc()

        context['countries'] = country_list
        context['game_desc'] = game_desc
        return context
