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
            # results = super(GameLookup, self).get_query(request, term)
            results = Game.objects.filter(platform=platform).filter(game__icontains=term)
            # results = results.filter(platform=platform)
            return results
        else:
            return ''


registry.register(GameLookup)
