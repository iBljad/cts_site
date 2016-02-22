from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Req, Platform, Game, Link, GamesDDForm
from .forms import GamesDD
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from datetime import timedelta
from django.utils import timezone


def index(request):
    reqs = Req.objects.order_by('-pub_date')[:15]
    platforms = Platform.objects.all()

    return render(request, 'cts_app/index.html', {'platforms': platforms, 'reqs': reqs})


def create(request, platform_id, error=''):
    try:
        platform = Platform.objects.get(pk=platform_id)
        link = Link.objects.filter(platform=platform).values('game')
        games = Game.objects.filter(id__in=link)
        form = GamesDD(games=games, platform=platform)
        error = error
    except Platform.DoesNotExist:
        raise Http404("Error occurred")

    return render(request, 'cts_app/create.html', {'games': games, 'forms': form, 'error': error})


def apply(request):
    if request.method == 'POST':
        f = GamesDDForm(request.POST)

        try:
            ttt = Req.objects.get(game=request.POST['game'], platform=request.POST['platform'],
                                  nickname=request.POST['nickname'],
                                  pub_date__gte=timezone.now() - timedelta(days=1))
            # return HttpResponse('Entry is duplicate, please try again...')
            return HttpResponseRedirect(
                reverse('cts_app:create_err', kwargs={'platform_id': request.POST['platform'],
                                                      'error': 'Error: Request with the same platform, game and nickname already exist'})
            )

        except Req.DoesNotExist:
            try:
                GamesDDForm.full_clean(f)
                new_req = f.save()
            except ValidationError as e:
                return HttpResponse(e.message_dict)

            else:
                return HttpResponseRedirect(reverse('cts_app:index'))

                # if request.method == 'POST':
                # 	f = GamesDDForm(request.POST)
                # 	new_req =f.save()
                # return HttpResponseRedirect(reverse('cts_app:index'))
