from __future__ import unicode_literals

from selectable.base import ModelLookup
from selectable.registry import registry

from .models import Game, Platform


class GameLookup(ModelLookup):
    model = Game

    def get_query(self, request, term):
        platform = request.GET.get('platform', '')
        if platform:
            results = Game.objects.filter(link__platform_id=platform, game__icontains=term)
        else:
            results = Game.objects.filter(game__icontains=term)
        return results


class PlatformLookup(ModelLookup):
    model = Platform

    def get_query(self, request, term):
        game = request.GET.get('game', '')
        if game:
            results = Platform.objects.filter(link__game_id=game, platform__icontains=term).order_by('platform')
        else:
            results = Platform.objects.filter(platform__icontains=term).order_by('platform')
        return results


registry.register(GameLookup)
registry.register(PlatformLookup)
