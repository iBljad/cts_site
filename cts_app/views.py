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
            ttt = Req.objects.filter(game=request.POST['game'], platform=request.POST['platform'],
                                     nickname=request.POST['nickname'].strip(),
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
            result = Req.objects.filter(game=request.POST['game'], platform=request.POST['platform'],
                                        nickname=request.POST['nickname'].strip())

        elif request.POST['game'] != '' and request.POST['platform'] != '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(game=request.POST['game'], platform=request.POST['platform'])

        elif request.POST['game'] != '' and request.POST['platform'] == '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(game=request.POST['game'], nickname=request.POST['nickname'].strip())

        elif request.POST['game'] != '' and request.POST['platform'] == '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(game=request.POST['game'])

        elif request.POST['game'] == '' and request.POST['platform'] != '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(platform=request.POST['platform'], nickname=request.POST['nickname'].strip())

        elif request.POST['game'] == '' and request.POST['platform'] != '' and request.POST['nickname'].strip() == '':
            result = Req.objects.filter(platform=request.POST['platform'])

        elif request.POST['game'] == '' and request.POST['platform'] == '' and request.POST['nickname'].strip() != '':
            result = Req.objects.filter(nickname=request.POST['nickname'].strip())

        else:
            return render(request, 'cts_app/search.html', {'forms': form, 'nbar': 'search',
                                                           'error': 'Please select at least one field to seacrh'})

    return render(request, 'cts_app/result.html', {'nbar': 'search', 'result': result})


def quicksearch(request):
    if request.method == 'POST':
        result = Req.objects.filter(
            Q(game__game=request.POST['query']) | Q(platform__platform=request.POST['query']) | Q(
                nickname=request.POST['query'].strip()))

    return render(request, 'cts_app/result.html', {'nbar': 'search', 'result': result})


def imp(request):
	games =  [{'game':'Alien Breed: Impact, Alien Breed 2: Assault, Alien Breed 3: Descent', 'date':'2010-01-01', 'platform':['PC']}	,
{'game':'Aliens versus Predator', 'date':'1999-01-01', 'platform':['PC']}	,
{'game':'Aliens versus Predator 2', 'date':'2001-01-01', 'platform':['PC']}	,
{'game':'Alien Shooter', 'date':'2003-01-01', 'platform':['PC']}	,
{'game':'Alien Swarm', 'date':'2010-01-01', 'platform':['PC']}	,
{'game':'Alpha Black Zero: Intrepid Protocol', 'date':'2004-01-01', 'platform':['PC']}	,
{'game':'Armed Assault', 'date':'2007-01-01', 'platform':['PC']}	,
{'game':'Armed Assault 2', 'date':'2009-01-01', 'platform':['PC']}	,
{'game':'Army of Two', 'date':'2008-01-01', 'platform':['PS3', 'Xbox 360', 'Sony PSP']}	,
{'game':'Army of Two: The 40th Day', 'date':'2010-01-01', 'platform':['PS3', 'Xbox 360']}	,
{'game':'Baldur\'s Gate', 'date':'1998-01-01', 'platform':['PC']}	,
{'game':'Baldur\'s Gate II: Shadows of Amn', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Battlefield 3', 'date':'2011-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Blazing Angels 2: Secret Missions of WWii', 'date':'2007-01-01', 'platform':['PC']}	,
{'game':'Blood', 'date':'1997-01-01', 'platform':['PC']}	,
{'game':'Blood 2', 'date':'1997-01-01', 'platform':['PC']}	,
{'game':'Borderlands', 'date':'2009-01-01', 'platform':['Xbox 360', 'PS3', 'PC']}	,
{'game':'Borderlands 2', 'date':'2012-01-01', 'platform':['Xbox 360', 'PS3', 'PC']}	,
{'game':'Borderlands: The Pre-Sequel', 'date':'2014-01-01', 'platform':['Xbox 360', 'PS3', 'PC']}	,
{'game':'Brink', 'date':'2011-01-01', 'platform':['Xbox 360', 'PS3', 'PC']}	,
{'game':'Brothers in Arms: Earned in Blood', 'date':'2005-01-01', 'platform':['PC', 'PS2', 'Xbox', 'Wii']}	,
{'game':'Call of Duty: World at War', 'date':'2008-01-01', 'platform':['PC', 'PS2', 'PS3', 'Xbox 360', 'Wii', 'NDS']}	,
{'game':'Call of Duty: Modern Warfare 2', 'date':'2009-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Call of Duty: Black Ops', 'date':'2010-01-01', 'platform':['PC', 'Xbox 360', 'PS3', 'Wii', 'NDS']}	,
{'game':'Call of Duty: Modern Warfare 3', 'date':'2011-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Call of Juarez: The Cartel', 'date':'2011-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Carnivores: Cityscape', 'date':'2002-01-01', 'platform':['PC']}	,
{'game':'Close Combat: First to Fight', 'date':'2005-01-01', 'platform':['PC']}	,
{'game':'Commandos 2', 'date':'2001-01-01', 'platform':['PC', 'PS2', 'Xbox']}	,
{'game':'Conflict: Global Storm', 'date':'2005-01-01', 'platform':['PC']}	,
{'game':'Conflict: Denied Ops', 'date':'2008-01-01', 'platform':['PC']}	,
{'game':'Crackdown', 'date':'2007-01-01', 'platform':['Xbox 360']}	,
{'game':'Cry of Fear', 'date':'2012-01-01', 'platform':['PC']}	,
{'game':'Daikatana', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Damnation', 'date':'2009-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Darkness II, The', 'date':'2012-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Dead Island', 'date':'2011-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Dead Island: Riptide', 'date':'2013-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Dead Space 3', 'date':'2013-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Deadly Dozen: Pacific Theatre', 'date':'2002-01-01', 'platform':['PC']}	,
{'game':'Delta Force', 'date':'1998-01-01', 'platform':['PC']}	,
{'game':'Delta Force 2', 'date':'1999-01-01', 'platform':['PC']}	,
{'game':'Delta Force: Land Warrior', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Delta Force: Task Force Dagger', 'date':'2002-01-01', 'platform':['PC']}	,
{'game':'Delta Force: Black Hawk Down', 'date':'2003-01-01', 'platform':['PC', 'PS2', 'Xbox']}	,
{'game':'Descent', 'date':'1995-01-01', 'platform':['PS']}	,
{'game':'Destiny', 'date':'2014-01-01', 'platform':['PS3','PS4','Xbox ONE' 'Xbox 360']}	,
{'game':'Diablo', 'date':'1996-01-01', 'platform':['PC', 'PS']}	,
{'game':'Diablo II', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Diablo III', 'date':'2012-01-01', 'platform':['PC', 'Mac', 'PS3', 'Xbox 360']}	,
{'game':'Doom', 'date':'1993-01-01', 'platform':['PC']}	,
{'game':'Doom II: Hell on Earth', 'date':'1994-01-01', 'platform':['PC']}	,
{'game':'Doom 3', 'date':'2004-01-01', 'platform':['PC', 'Xbox']}	,
{'game':'Duke Nukem 3D', 'date':'1996-01-01', 'platform':['PC', 'PS', 'N64', 'Sega Saturn']}	,
{'game':'Dungeon Siege', 'date':'2002-01-01', 'platform':['PC']}	,
{'game':'Dungeon Siege II', 'date':'2005-01-01', 'platform':['PC']}	,
{'game':'Dungeon Siege III', 'date':'2011-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Dungeon Lords', 'date':'2005-01-01', 'platform':['PC']}	,
{'game':'Dying Light', 'date':'2015-01-01', 'platform':['PC', 'PS4', 'Xbox ONE']}	,
{'game':'Eagle One: Harrier Attack', 'date':'2000-01-01', 'platform':['PS']}	,
{'game':'Far Cry', 'date':'2004-01-01', 'platform':['PC']}	,
{'game':'Far Cry 3', 'date':'2012-01-01', 'platform':['PC']}	,
{'game':'Far Cry 4', 'date':'2014-01-01', 'platform':['PC', 'Xbox ONE', 'PS4', 'Xbox 360', 'PS3']}	,
{'game':'F.E.A.R.', 'date':'2005-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'F.E.A.R.3', 'date':'2011-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Tom Clancy\’s Rainbow Six: Vegas 2', 'date':'2008-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Freelancer', 'date':'2003-01-01', 'platform':['PC']}	,
{'game':'Full Spectrum Warrior', 'date':'2004-01-01', 'platform':['PC', 'PS2', 'Xbox']}	,
{'game':'Gauntlet: Seven Sorrows', 'date':'1997-01-01', 'platform':['PS2', 'Xbox', 'Xbox 360']}	,
{'game':'Gears of War', 'date':'2006-01-01', 'platform':['PC', 'Xbox 360']}	,
{'game':'Gears of War 2', 'date':'2008-01-01', 'platform':['Xbox 360']}	,
{'game':'Gears of War 3', 'date':'2011-01-01', 'platform':['Xbox 360']}	,
{'game':'God Mode', 'date':'2013-01-01', 'platform':['PC', 'Xbox 360', 'PS3']}	,
{'game':'Golden Axe 1, 2, 3', 'date':'1995-01-01', 'platform':['PC']}	,
{'game':'Greed: Black Border', 'date':'2009-01-01', 'platform':['PC']}	,
{'game':'Ground Control 2: Operation Exodus', 'date':'2004-01-01', 'platform':['PC']}	,
{'game':'Half-Life', 'date':'1998-01-01', 'platform':['PC', 'PS2']}	,
{'game':'Half-Life: Decay', 'date':'2001-01-01', 'platform':['PC', 'PS2']}	,
{'game':'Half-Life 2', 'date':'2004-01-01', 'platform':['PC', 'Xbox', 'Xbox 360', 'PS3']}	,
{'game':'Halo 3, Halo 3: ODST, Halo: Reach', 'date':'2010-01-01', 'platform':['Xbox 360']}	,
{'game':'Haunted: Hells Reach, The', 'date':'2011-01-01', 'platform':['PC', 'Xbox 360']}	,
{'game':'Haze', 'date':'2008-01-01', 'platform':['PS3']}	,
{'game':'Hellgate: London', 'date':'2007-01-01', 'platform':['PC']}	,
{'game':'Heretic 1', 'date':'1994-01-01', 'platform':['PC']}	,
{'game':'Heretic 2', 'date':'1998-01-01', 'platform':['PC']}	,
{'game':'Hexen 1', 'date':'1995-01-01', 'platform':['PC', 'PS', 'N64', 'Sega Saturn']}	,
{'game':'Hexen 2', 'date':'1997-01-01', 'platform':['PC']}	,
{'game':'Hidden & Dangerous Deluxe', 'date':'1999-01-01', 'platform':['PC']}	,
{'game':'Hidden and Dangerous 2: Sabre Squadron', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Hunted: The Demon\'s Forge', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Icewind Dale', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Icewind Dale 2', 'date':'2002-01-01', 'platform':['PC']}	,
{'game':'Joint Task Force', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Killing Floor', 'date':'2009-01-01', 'platform':['PC']}	,
{'game':'Kane & Lynch 2: Dog Days', 'date':'2010-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Land Of The Dead', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Lara Croft and the Guardian of Light', 'date':'2010-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Left 4 Dead', 'date':'2008-01-01', 'platform':['PC', 'Xbox 360']}	,
{'game':'Left 4 Dead 2', 'date':'2009-01-01', 'platform':['PC', 'Xbox 360']}	,
{'game':'Line of Sight: Vietnam', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Loki: Heroes of Mythology', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Lord of the rings: Return of the King, Lord of the rings: Conquest,Lord of the rings: War in the North', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Lost Planet 2', 'date':'2010-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'LittleBigPlanet', 'date':'2008-01-01', 'platform':['PS3']}	,
{'game':'Mage Knight: Apocalypse', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Magicka', 'date':'2011-01-01', 'platform':['PC']}	,
{'game':'Mass Effect 3', 'date':'2012-01-01', 'platform':['PC', 'Xbox 360','PS3']}	,
{'game':'Men of War: Vietnam', 'date':'2011-01-01', 'platform':['PC']}	,
{'game':'Minecraft', 'date':'2009-01-01', 'platform':['PC', 'Xbox 360','PS3','Android', 'iOS']}	,
{'game':'Neverwinter Nights', 'date':'2002-01-01', 'platform':['PC']}	,
{'game':'Neverwinter Nights 2', 'date':'2006-01-01', 'platform':['PC']}	,
{'game':'No One Lives Forever 2', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Operation Flashpoint: Cold War Crisis', 'date':'2001-01-01', 'platform':['PC']}	,
{'game':'Operation Flashpoint: Dragon Rising', 'date':'2009-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Operation Flashpoint: Red River', 'date':'2011-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Painkiller: Hell & Damnation', 'date':'2012-01-01', 'platform':['PC', 'Mac']}	,
{'game':'Payday: The Heist', 'date':'2011-01-01', 'platform':['PC', 'PS3']}	,
{'game':'Portal 2', 'date':'2011-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Project Eden', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Quake', 'date':'1996-01-01', 'platform':['PC', 'Sega Saturn', 'N64']}	,
{'game':'Quake 2', 'date':'1997-01-01', 'platform':['PC', 'PS', 'N64']}	,
{'game':'Resident Evil 5', 'date':'2009-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Resident Evil 6', 'date':'2013-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Red Alert 3', 'date':'2008-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Redneck Rampage', 'date':'1997-01-01', 'platform':['PC']}	,
{'game':'Rogue Trooper', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Sacred', 'date':'2004-01-01', 'platform':['PC']}	,
{'game':'Sacred 2: Fallen Angel', 'date':'2008-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Samurai Warriors 2', 'date':'2006-01-01', 'platform':['PC', 'PS2', 'Xbox 360']}	,
{'game':'Saints Row 2', 'date':'2008-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Saints Row: The Third', 'date':'2011-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Saints Row IV', 'date':'2013-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Saints Row: Gat out of Hell', 'date':'2015-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Sniper Elite V2', 'date':'2012-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Tom Clancy\’s Splinter Cell: Chaos Theory', 'date':'2005-01-01', 'platform':['PC', 'PS2', 'PS3', 'Xbox', 'NDS', 'GCN']}	,
{'game':'Tom Clancy\’s Splinter Cell: Double Agent', 'date':'2006-01-01', 'platform':['PC', 'PS2', 'PS3', 'Xbox', 'Xbox 360', 'Wii', 'GCN']}	,
{'game':'Tom Clancy\’s Splinter Cell: Conviction', 'date':'2010-01-01', 'platform':['PC', 'Xbox 360']}	,
{'game':'Tom Clancy\’s Splinter Cell: Blacklist', 'date':'2013-01-01', 'platform':['PC']}	,
{'game':'Serious Sam 1', 'date':'2002-01-01', 'platform':['PC', 'Xbox', 'Xbox 360', 'PS2', 'GCN', 'GBA']}	,
{'game':'Serious Sam 2', 'date':'2005-01-01', 'platform':['PC', 'Xbox']}	,
{'game':'Serious Sam HD', 'date':'2010-01-01', 'platform':['PC', 'Xbox 360']}	,
{'game':'Shadow Warrior', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Shadowgrounds Survivor', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Space Station 13', 'date':'2015-01-01', 'platform':['PC']}	,
{'game':'SpellForce', 'date':'2003-01-01', 'platform':['PC']}	,
{'game':'SpellForce 2', 'date':'2006-01-01', 'platform':['PC']}	,
{'game':'Starship Troopers', 'date':'2005-01-01', 'platform':['PC']}	,
{'game':'System Shock 2', 'date':'1999-01-01', 'platform':['PC']}	,
{'game':'SWAT 3', 'date':'1999-01-01', 'platform':['PC']}	,
{'game':'SWAT 4', 'date':'2005-01-01', 'platform':['PC']}	,
{'game':'Teenage Mutant Ninja Turtles (1,2,3 части от KONAMI)', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Terraria', 'date':'2011-01-01', 'platform':['PC']}	,
{'game':'The Chronicles of Narnia: The Lion, the Witch and the Wardrobe', 'date':'2005-01-01', 'platform':['PC', 'PS2', 'Xbox', 'NDS', 'GCN', 'GBA']}	,
{'game':'The Chronicles of Narnia: Prince Caspian', 'date':'2008-01-01', 'platform':['PC', 'PS2', 'PS3', 'Xbox 360', 'NDS', 'Wii']}	,
{'game':'The First Templar', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'The Forest', 'date':'2014-01-01', 'platform':['PC']}	,
{'game':'The Mark', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'The Regiment', 'date':'2006-01-01', 'platform':['PC']}	,
{'game':'The Scourge Project: Episode 1 and 2', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Titan Quest, Titan Quest: Immortal Throne', 'date':'2007-01-01', 'platform':['PC']}	,
{'game':'Tom Clancy\’s Ghost Recon', 'date':'2001-01-01', 'platform':['PC', 'PS2', 'Xbox', 'GCN']}	,
{'game':'Tom Clancy\’s Ghost Recon: Advanced Warfighter 2', 'date':'2007-01-01', 'platform':['PC']}	,
{'game':'Tom Clancy\’s Ghost Recon: Future Soldier', 'date':'2012-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Tom Clancy\’s H.A.W.X.', 'date':'2009-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Tom Clancy\’s Rainbow Six', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Torchlight II', 'date':'2011-01-01', 'platform':['PC']}	,
{'game':'Trapped Dead', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'Transformers: War for Cybertron', 'date':'2010-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Transformers: Fall of Cybertron', 'date':'2012-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Trine 2', 'date':'2011-01-01', 'platform':['PC', 'Mac']}	,
{'game':'Twisted Metal 2', 'date':'1996-01-01', 'platform':['PS', 'PC', 'PS3']}	,
{'game':'Twisted Metal 3, Twisted Metal 4', 'date':'1999-01-01', 'platform':['PS']}	,
{'game':'Twisted Metal Black', 'date':'2001-01-01', 'platform':['PS2', 'PS3']}	,
{'game':'Twisted Metal (2012-01-01)', 'date':'2012-01-01', 'platform':['PS3']}	,
{'game':'Two Worlds II', 'date':'2010-01-01', 'platform':['PC', 'PS3', 'Xbox 360']}	,
{'game':'Unreal', 'date':'1998-01-01', 'platform':['PC']}	,
{'game':'Vietcong', 'date':'2003-01-01', 'platform':['PC']}	,
{'game':'Vietcong 2', 'date':'2005-01-01', 'platform':['PC']}	,
{'game':'Venom: Codename Outbreak', 'date':'2001-01-01', 'platform':['PC']}	,
{'game':'Warhammer 40,000: Dawn of War II, Warhammer 40,000: Dawn of War II: Chaos Rising', 'date':'2010-01-01', 'platform':['PC']}	,
{'game':'Will Rock', 'date':'2003-01-01', 'platform':['PC']}	,
{'game':'WorldShift/EdY', 'date':'2000-01-01', 'platform':['PC']}	,
{'game':'В тылу врага', 'date':'2004-01-01', 'platform':['PC']}	,
{'game':'В тылу врага 2, В тылу врага 2: Братья по оружию,В тылу врага 2: Лис пустыни', 'date':'2009-01-01', 'platform':['PC']}	,
{'game':'Ил-2 Штурмовик', 'date':'2001-01-01', 'platform':['PC']}
]

	for item in games:
		current_game, created = Game.objects.get_or_create(game=item['game'], release_date=item['date'])
		for nplatform in item['platform']:
			current_platform,created = Platform.objects.get_or_create(platform=nplatform)
			Link.objects.get_or_create(game=current_game, platform=current_platform, 
				link_name=(current_game.game + ' - ' + current_platform.platform))

	return HttpResponse("Hi")
