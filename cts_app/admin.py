from django.contrib import admin

# Register your models here.
from .models import Game, Platform, Link, Req

admin.site.register(Game)
admin.site.register(Platform)
admin.site.register(Link)
admin.site.register(Req)