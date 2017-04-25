from __future__ import unicode_literals

from selectable.base import ModelLookup
from selectable.registry import registry

from .models import Game


class GameLookup(ModelLookup):
    model = Game
    search_fields = ('game__icontains',)

    def get_query(self, request, term):
        platform = request.GET.get('platform', '')
        if platform:
            results = Game.objects.select_related('platform').filter(platform=platform).filter(game__icontains=term)
            return results
        else:
            results = Game.objects.select_related('platform').filter(game__icontains=term).distinct('game')
            results = list(results)
            for game in results:
                game.game = game.game + ' (' + game.platform.platform + ')'
            return ''


registry.register(GameLookup)
