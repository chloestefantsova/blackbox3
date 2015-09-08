from django.shortcuts import get_object_or_404

from game.models import Game


def get_game(raise_exception=True):
    if raise_exception:
        return get_object_or_404(Game, pk__isnull=False)
    games = Game.objects.all()
    if len(games) != 1:
        return None
    return games[0]
