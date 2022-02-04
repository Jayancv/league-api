from django.contrib import admin

# Register your models here.
from game.models import Tournament, Match

admin.site.register(Tournament)
admin.site.register(Match)