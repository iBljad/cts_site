from django.db import models
from django.forms import ModelForm


class Platform(models.Model):
    platform = models.CharField(max_length=20)

    def __str__(self):
        return self.platform


class Game(models.Model):
    game = models.CharField(max_length=1000)
    release_date = models.DateField('release date')

    def __str__(self):
        return self.game


class Link(models.Model):
    platform = models.ForeignKey(Platform)
    game = models.ForeignKey(Game)
    link_name = models.CharField('Link Name', max_length=1000)

    def __str__(self):
        return self.link_name


class Req(models.Model):
    platform = models.ForeignKey(Platform)
    game = models.ForeignKey(Game)
    nickname = models.CharField(max_length=20)
    comment = models.CharField(max_length=280)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pub_date.__str__()


class GamesDDForm(ModelForm):
    class Meta:
        model = Req
        exclude = ['pub_date']
