from django.contrib import admin

# Register your models here.
from apibasics.models import User, Player, Coach

admin.site.register(User)
admin.site.register(Player)
admin.site.register(Coach)