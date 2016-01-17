from django.contrib import admin

from . import models
from .models import Game, Team, Player, Stats, Week, TourneyCode
# Register your models here.

admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Stats)
admin.site.register(Player)
admin.site.register(Week)
admin.site.register(TourneyCode)