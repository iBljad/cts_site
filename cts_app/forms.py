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
    platform = forms.ChoiceField()
    nickname = forms.CharField(max_length=20)
    comment = forms.CharField(max_length=280)

    def __init__(self, *args, **kwargs):
        self.games_list = kwargs.pop('games')
        self.platform_id = kwargs.pop('platform')
        # self.game = forms.ChoiceField()
        super(GamesDD, self).__init__(*args, **kwargs)
        self.fields['game'].choices = [(p.pk, p.game) for p in self.games_list]
        self.fields['platform'].choices = [(p.pk, p.platform) for p in [self.platform_id]]
        self.fields['platform'].initial = self.platform_id
        self.fields['platform'].widget.attrs['readonly'] = True
