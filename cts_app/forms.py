from django import forms
from selectable.forms import AutoCompleteSelectField, AutoCompleteSelectWidget

from .lookups import GameLookup, PlatformLookup
from .models import Platform


class SearchForm(forms.Form):
    # platforms = [('', 'Platform')] + [(p.pk, p.platform) for p in Platform.objects.all()]
    # # games = [(p.pk, p.game) for p in Game.objects.all()] + [('', 'Game')]
    platform = AutoCompleteSelectField(
        label='Platform',
        widget=AutoCompleteSelectWidget(lookup_class=PlatformLookup,
                                        attrs={'class': 'form-control', 'placeholder': 'Platform',
                                               'data-selectable-options': {'minLength': 0}}),
        required=False,
        lookup_class=PlatformLookup,
    )
    game = AutoCompleteSelectField(
        label='Game',
        widget=AutoCompleteSelectWidget(lookup_class=GameLookup,
                                        attrs={'class': 'form-control', 'placeholder': 'Game'}), required=False,
        lookup_class=GameLookup,
    )
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),
                               max_length=20, required=False)


class NewSearchForm(forms.Form):
    game = AutoCompleteSelectField(
        label='Game',
        widget=AutoCompleteSelectWidget(lookup_class=GameLookup,
                                        attrs={'class': 'form-control', 'placeholder': 'Game'}), required=False,
        lookup_class=GameLookup,
    )


class ReqPostForm(forms.Form):
    platform = AutoCompleteSelectField(
        label='Platform',
        widget=AutoCompleteSelectWidget(lookup_class=PlatformLookup,
                                        attrs={'class': 'form-control', 'placeholder': 'Platform',
                                               'data-selectable-options': {'minLength': 0}}),
        required=False,
        lookup_class=PlatformLookup,
    )
    game = AutoCompleteSelectField(
        label='Game',
        widget=AutoCompleteSelectWidget(lookup_class=GameLookup,
                                        attrs={'class': 'form-control', 'placeholder': 'Game'}),
        lookup_class=GameLookup, required=True
    )
    comment = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}), initial='',
                              required=False)


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
