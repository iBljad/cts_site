from datetime import timedelta
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models import Avg, Count
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils import timezone
from .forms import GamesDD, SearchForm, UserVote, ContactForm
from .models import Req, Platform, Game, Link, GamesDDForm, RegisterForm, LoginForm, Votes


def index(request):
    form = ContactForm
    # reqs = Req.objects.filter(active=True).order_by('-pub_date')[:15]
    # platforms = Platform.objects.all()
    messages.debug(request, 'Test')

    return render(request, 'cts_app/index.html',
                  {''' 'platforms': platforms,  'reqs': reqs,''' 'nbar': 'home'})


def create(request):
    try:
        platform_id = request.GET['platform_id']
        platform = Platform.objects.get(pk=platform_id)
        link = Link.objects.filter(platform=platform).values('game')
        games = Game.objects.filter(id__in=link)
        form = GamesDD(user=request.user, games=games, platform=platform)
    except Platform.DoesNotExist:
        raise Http404("Error occurred")

    return render(request, 'cts_app/create.html', {'games': games, 'forms': form, 'nbar': 'create'})


def apply(request):
    if request.method == 'POST':

        f = GamesDDForm(request.POST)
        GamesDDForm.full_clean(f)

        try:
            ttt = Req.objects.get(active=True, game=request.POST['game'], platform=request.POST['platform'],
                                  nickname=request.user,
                                  pub_date__gte=timezone.now() - timedelta(days=1))
            # return HttpResponse('Entry is duplicate, please try again...')
            messages.warning(request, 'Request with the same platform, game and nickname already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        except Req.DoesNotExist:
            try:
                f.save()
            except ValidationError as e:
                return HttpResponse(e.message_dict)

            else:
                messages.success(request, 'Your request was successfully posted')
                return HttpResponseRedirect(reverse('cts_app:index'))


def search(request):
    form = SearchForm()

    return render(request, 'cts_app/search.html', {'forms': form, 'nbar': 'search'})


def result(request, error=''):
    form = SearchForm()
    if request.method == 'POST':
        if request.POST['game'] != '' and request.POST['platform'] != '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(active=True, game=request.POST['game'], platform=request.POST['platform'],
                                        nickname__username__iexact=request.POST['nickname'].strip()).order_by(
                '-pub_date')

        elif request.POST['game'] != '' and request.POST['platform'] != '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(active=True, game=request.POST['game'],
                                        platform=request.POST['platform']).order_by('-pub_date')

        elif request.POST['game'] != '' and request.POST['platform'] == '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(active=True, game=request.POST['game'],
                                        nickname__username__iexact=request.POST['nickname'].strip()).order_by(
                '-pub_date')

        elif request.POST['game'] != '' and request.POST['platform'] == '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(active=True, game=request.POST['game']).order_by('-pub_date')

        elif request.POST['game'] == '' and request.POST['platform'] != '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(active=True, platform=request.POST['platform'],
                                        nickname__username__iexact=request.POST['nickname'].strip()).order_by(
                '-pub_date')

        elif request.POST['game'] == '' and request.POST['platform'] != '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(active=True, platform=request.POST['platform']).order_by('-pub_date')

        elif request.POST['game'] == '' and request.POST['platform'] == '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(active=True,
                                        nickname__username__iexact=request.POST['nickname'].strip()).order_by(
                '-pub_date')

        else:
            messages.warning(request, 'Please select at least one field to search')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'cts_app/result.html', {'nbar': 'search', 'result': result})


def quicksearch(request):
    if request.method == 'POST':
        result = Req.objects.filter(
            Q(active=True, game__game__icontains=request.POST['query']) |
            Q(active=True, platform__platform__icontains=request.POST['query']) |
            Q(active=True, nickname__username__icontains=request.POST['query'].strip()))

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
                form.add_error('email', 'Email already exists')
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
                messages.success(request, 'You were successfully registered, thanks!')
                return HttpResponseRedirect(reverse('cts_app:index'))

        else:
            return render(request, 'cts_app/login.html',
                          {'nbar': 'Log in/register', 'forms': form, 'forms2': LoginForm()})
    else:
        messages.error(request, 'Oops, something went wrong')
        return HttpResponseRedirect(reverse('cts_app:index'))


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    messages.success(request, 'You were successfully logged out')
    return HttpResponseRedirect(reverse('cts_app:index'))


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
            messages.success(request, 'You were successfully logged in')
            return HttpResponseRedirect(reverse('cts_app:index'))
        else:
            # Return a 'disabled account' error message
            messages.error(request, 'Your account was disabled')
            return render(request, 'cts_app/login.html',
                          {'nbar': 'Log in/register', 'forms': RegisterForm(), 'forms2': LoginForm()})
            # TODO Return an 'invalid login' error message.
    else:
        messages.error(request, 'Invalid login or password')
        return render(request, 'cts_app/login.html',
                      {'nbar': 'Log in/register', 'forms': RegisterForm(), 'forms2': LoginForm()})


def profile(request, user):
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        raise Http404("User doesnt exists")

    form = UserVote(user=user, voted_user=request.user)
    votes = Votes.objects.filter(user=user).order_by('-pub_date')

    platforms = Platform.objects.select_related('Req').filter(req__nickname=user).values('platform').annotate(
        count=Count('platform')).order_by('-count')

    games = Game.objects.select_related('Req').filter(req__nickname=user).values('game').annotate(
        count=Count('game')).order_by('-count')

    reqs = Req.objects.filter(active=True, nickname=user.id).order_by('-pub_date')[:15]

    rating = Votes.objects.filter(user=user).aggregate(Avg('rate'))['rate__avg']

    return render(request, 'cts_app/profile.html', {'nbar': 'profile', 'user1': user, 'forms': form, 'votes': votes,
                                                    'rating': rating, 'reqs': reqs, 'platforms': platforms,
                                                    'games': games})


def vote(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['user'])
            voted_user = User.objects.get(username=request.POST['voted_user'])
        except User.DoesNotExist:
            raise Http404("User doesnt exists")
        else:
            try:
                vote = Votes.objects.get(user=user, voted_user=voted_user)

            except Votes.DoesNotExist:
                Votes.objects.create(user=user, voted_user=voted_user, rate=request.POST['rate'],
                                     comment=request.POST['comment'])
            else:
                vote.rate = request.POST['rate']
                vote.comment = request.POST['comment']
                vote.pub_date = timezone.now()
                vote.save(update_fields=['rate', 'comment', 'pub_date'])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def reqdel(request, req_id):
    if request.user.username == Req.objects.get(id=req_id).nickname.__str__():
        Req.objects.filter(id=req_id).update(active=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def top(request, entity):
    if entity == 'platform':
        result = Platform.objects.select_related('Req').filter(req__nickname__gte=0).values('platform').annotate(
            count=Count('platform')).order_by('-count')[:10]

    elif entity == 'game':
        result = Game.objects.select_related('Req').filter(req__nickname__gte=0).values('game').annotate(
            count=Count('game')).order_by('-count')[:10]
    elif entity == 'user':
        result = User.objects.select_related('Req').filter(req__nickname__gte=0).values('username').annotate(
            count=Count('username')).order_by('-count')[:10]
    return render(request, 'cts_app/tops.html', {'nbar': 'tops', 'entity': entity, 'result': result})


def contact(request):
    form = ContactForm
    return render(request, 'cts_app/contact.html', {'nbar': 'contact', 'forms': form})


def send_email(request):
    form = ContactForm(request.POST)
    subject = '[CTS] ' + request.POST['subject']
    from_email = request.POST['email']
    if from_email:
        message = request.POST['email'] + ': \n' + request.POST['message']
    else:
        message = request.POST['message']
    if subject and message:
        try:
            send_mail(subject, message, 'goplaycoop@yandex.ru', ['drakonmail@gmail.com'], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        messages.success(request, 'Your message was sent, thanks!')
        return HttpResponseRedirect(reverse('cts_app:index'))
    else:
        return render(request, 'cts_app/contact.html', {'nbar': 'contact', 'forms': form})
