from django import forms
from .models import Req, Game, Platform, Link


class radioForm(forms.Form):
    games = Game.objects.all()


class NameForm(forms.Form):
    RADIO_CHOICES = [['1', 'Radio 1'], ['2', 'Radio 2']]
    games = forms.ChoiceField(widget=forms.RadioSelect, choices=
    [(p.pk, p.platform) for p in Platform.objects.all()]
                              )

    def is_valid(x):
        return True


class GamesDD(forms.Form):
    game = forms.ChoiceField()
    platform = forms.ChoiceField(widget=forms.HiddenInput())
    nickname = forms.CharField(max_length=20)
    comment = forms.CharField(max_length=280, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
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

class SearchForm(forms.Form):
	platforms = [(p.pk, p.platform) for p in Platform.objects.all()] + [('','---------')]
	games = [(p.pk, p.game) for p in Game.objects.all()] + [('','---------')]
	platform = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),
		choices=platforms)
	game = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),
		choices=games)
	nickname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=20)
