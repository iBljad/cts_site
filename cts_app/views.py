from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Req, Platform, Game, Link, GamesDDForm, SearchFormModel, RegisterForm, LoginForm
from .forms import GamesDD, SearchForm
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User, Permission
from django.contrib.auth import logout, authenticate, login


def index(request, message=None):
    reqs = Req.objects.order_by('-pub_date')[:15]
    platforms = Platform.objects.all()
    message = message

    return render(request, 'cts_app/index.html',
                  {'platforms': platforms, 'reqs': reqs, 'nbar': 'home', 'message': message})


def create(request, platform_id, error=''):
    try:
        platform = Platform.objects.get(pk=platform_id)
        link = Link.objects.filter(platform=platform).values('game')
        games = Game.objects.filter(id__in=link)
        form = GamesDD(user=request.user, games=games, platform=platform)
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
                                  nickname=request.user,
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
                return index(request, message='Your request has been succesfully posted')

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
            result = Req.objects.filter(game=request.POST['game'], platform=request.POST['platform'],
                                        nickname__username__iexact=request.POST['nickname'].strip())

        elif request.POST['game'] != '' and request.POST['platform'] != '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(game=request.POST['game'], platform=request.POST['platform'])

        elif request.POST['game'] != '' and request.POST['platform'] == '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(game=request.POST['game'],
                                        nickname__username__iexact=request.POST['nickname'].strip())

        elif request.POST['game'] != '' and request.POST['platform'] == '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(game=request.POST['game'])

        elif request.POST['game'] == '' and request.POST['platform'] != '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(platform=request.POST['platform'],
                                        nickname__username__iexact=request.POST['nickname'].strip())

        elif request.POST['game'] == '' and request.POST['platform'] != '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(platform=request.POST['platform'])

        elif request.POST['game'] == '' and request.POST['platform'] == '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(nickname__username__iexact=request.POST['nickname'].strip())

        else:
            return render(request, 'cts_app/search.html', {'forms': form, 'nbar': 'search',
                                                           'error': 'Please select at least one field to seacrh'})

    return render(request, 'cts_app/result.html', {'nbar': 'search', 'result': result})


def quicksearch(request):
    if request.method == 'POST':
        result = Req.objects.filter(
            Q(game__game__icontains=request.POST['query']) | Q(platform__platform__icontains=request.POST['query']) | Q(
                nickname__username__icontains=request.POST['query'].strip()))

    return render(request, 'cts_app/result.html', {'nbar': 'search', 'result': result})


def test1(request):
    form = RegisterForm()
    return render(request, 'cts_app/test1.html', {'nbar': 'search', 'forms': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                ttt = User.objects.get(email=form.cleaned_data['email'])
                form.add_error('email', 'This email already exists')
                return render(request, 'cts_app/login.html',
                              {'nbar': 'Log in/register', 'forms': form, 'forms2': LoginForm()})
            except User.DoesNotExist:
                u = User.objects.create_user(username=form.cleaned_data['username'],
                                             email=form.cleaned_data['email'],
                                             password=form.cleaned_data['password'])
                p1 = Permission.objects.get(name__icontains='Can add req')
                p2 = Permission.objects.get(name__icontains='Can change req')
                p3 = Permission.objects.get(name__icontains='Can delete req')
                u.user_permissions.add(p1, p2, p3)

                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                login(request, user)
                return index(request, message='You were succesfully registered, thanks!')

        else:
            return render(request, 'cts_app/login.html',
                          {'nbar': 'Log in/register', 'forms': form, 'forms2': LoginForm()})
    else:
        return index(request, message='Oops, something went wrong')


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return index(request, message='You were succesfully logged out')


def login_page(request):
    return render(request, 'cts_app/login.html',
                  {'nbar': 'Log in/register', 'forms': RegisterForm(), 'forms2': LoginForm()})


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return index(request, message='You were succesfully logged in')
        else:
            # Return a 'disabled account' error message
            return render(request, 'cts_app/login.html', {'nbar': 'Log in/register', 'forms': form, 'forms2': form2,
                                                          'error2': 'Your account was disabled'})
            # Return an 'invalid login' error message.
    else:
        return render(request, 'cts_app/login.html',
                      {'nbar': 'Log in/register', 'forms': RegisterForm(), 'forms2': LoginForm(),
                       'error2': 'Invalid login or password'})


def profile(request, user):
    return render(request, 'cts_app/profile.html', {'nbar': 'Profile'})
