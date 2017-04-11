from __future__ import unicode_literals

from selectable.base import ModelLookup
from selectable.registry import registry

from .models import Game, Link


class GameLookup(ModelLookup):
    model = Game
    search_fields = ('game__icontains',)

    def get_query(self, request, term):
        results = super(GameLookup, self).get_query(request, term)
        platform = request.GET.get('platform', '')
        if platform:
            link = Link.objects.filter(platform=platform).values('game')
            results = Game.objects.filter(id__in=link).filter(game__icontains=term)
            # results = results.filter(platform=platform)
        return results


registry.register(GameLookup)
