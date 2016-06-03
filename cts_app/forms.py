from django import forms
from .models import Req, Game, Platform, Link


class GamesDD(forms.Form):
    game = forms.ChoiceField()
    platform = forms.ChoiceField(widget=forms.HiddenInput())
    nickname = forms.CharField(widget=forms.HiddenInput())
    comment = forms.CharField(max_length=280, widget=forms.Textarea(), initial='')
    active = forms.BooleanField(initial=True, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.nickname = kwargs.pop('user')
        self.games_list = kwargs.pop('games')
        self.platform_id = kwargs.pop('platform')
        # self.game = forms.ChoiceField()
        super(GamesDD, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['game'].choices = [(p.pk, p.game) for p in self.games_list]
        self.fields['platform'].choices = [(p.pk) for p in [self.platform_id]]
        self.fields['platform'].initial = self.platform_id.id
        self.fields['nickname'].initial = self.nickname.id


class SearchForm(forms.Form):
    platforms = [(p.pk, p.platform) for p in Platform.objects.all()] + [('', '---------')]
    games = [(p.pk, p.game) for p in Game.objects.all()] + [('', '---------')]
    platform = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                 choices=platforms)
    game = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             choices=games)
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=20)


class UserVote(forms.Form):
    my_choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

    user = forms.CharField(widget=forms.HiddenInput())
    voted_user = forms.CharField(widget=forms.HiddenInput())
    rate = forms.ChoiceField(choices=my_choices)
    comment = forms.CharField(max_length=1000, widget=forms.Textarea(), initial='')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.voted_user = kwargs.pop('voted_user')
        super(UserVote, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['user'].initial = self.user
        self.fields['voted_user'].initial = self.voted_user


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, required=False)
    message = forms.CharField(widget=forms.Textarea, max_length=4000)
    email = forms.EmailField(required=False, max_length=200)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
