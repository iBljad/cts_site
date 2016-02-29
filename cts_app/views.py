from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Req, Platform, Game, Link, GamesDDForm, SearchFormModel
from .forms import GamesDD, SearchForm
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q


def index(request):
    reqs = Req.objects.order_by('-pub_date')[:15]
    platforms = Platform.objects.all()

    return render(request, 'cts_app/index.html', {'platforms': platforms, 'reqs': reqs, 'nbar': 'home'})


def create(request, platform_id, error=''):
    try:
        platform = Platform.objects.get(pk=platform_id)
        link = Link.objects.filter(platform=platform).values('game')
        games = Game.objects.filter(id__in=link)
        form = GamesDD(games=games, platform=platform)
        error = error
    except Platform.DoesNotExist:
        raise Http404("Error occurred")

    return render(request, 'cts_app/create.html', {'games': games, 'forms': form, 'error': error, 'nbar': 'create'})


def apply(request):
    if request.method == 'POST':
        f = GamesDDForm(request.POST)
        GamesDDForm.full_clean(f)

        try:
            ttt = Req.objects.get(game=request.POST['game'], platform=request.POST['platform'],
                                     nickname__iexact=request.POST['nickname'].strip(),
                                     pub_date__gte=timezone.now() - timedelta(days=1))
            # return HttpResponse('Entry is duplicate, please try again...')
            return HttpResponseRedirect(
                reverse('cts_app:create_err', kwargs={'platform_id': request.POST['platform'],
                                                      'error': 'Request with the same platform, game and nickname already exist'})
            )

        except Req.DoesNotExist:
            try:
                f.save()
            except ValidationError as e:
                return HttpResponse(e.message_dict)

            else:
                return HttpResponseRedirect(reverse('cts_app:index'))
                
                # if request.method == 'POST':
                # 	f = GamesDDForm(request.POST)
                # 	new_req =f.save()
                # return HttpResponseRedirect(reverse('cts_app:index'))


def search(request):
    form = SearchForm()

    return render(request, 'cts_app/search.html', {'forms': form, 'nbar': 'search'})


def result(request, error=''):
    form = SearchForm()
    if request.method == 'POST':
        if request.POST['game'] != '' and request.POST['platform'] != '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(game__iexact=request.POST['game'], platform__iexact=request.POST['platform'],
                                        nickname__iexact=request.POST['nickname'].strip())

        elif request.POST['game'] != '' and request.POST['platform'] != '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(game__iexact=request.POST['game'], platform__iexact=request.POST['platform'])

        elif request.POST['game'] != '' and request.POST['platform'] == '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(game__iexact=request.POST['game'], nickname__iexact=request.POST['nickname'].strip())

        elif request.POST['game'] != '' and request.POST['platform'] == '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(game__iexact=request.POST['game'])

        elif request.POST['game'] == '' and request.POST['platform'] != '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(platform__iexact=request.POST['platform'], nickname__iexact=request.POST['nickname'].strip())

        elif request.POST['game'] == '' and request.POST['platform'] != '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(platform__iexact=request.POST['platform'])

        elif request.POST['game'] == '' and request.POST['platform'] == '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(nickname__iexact=request.POST['nickname'].strip())

        else:
            return render(request, 'cts_app/search.html', {'forms': form, 'nbar': 'search',
                                                           'error': 'Please select at least one field to seacrh'})

    return render(request, 'cts_app/result.html', {'nbar': 'search', 'result': result})


def quicksearch(request):
    if request.method == 'POST':
        result = Req.objects.filter(
            Q(game__game__icontains=request.POST['query']) | Q(platform__platform__icontains=request.POST['query']) | Q(
                nickname__icontains=request.POST['query'].strip()))

    return render(request, 'cts_app/result.html', {'nbar': 'search', 'result': result})


