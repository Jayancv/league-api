from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import Avg, F, Count

from team.models import Team


# This user extend from Basic user to manage authentication
class User(AbstractUser):
    CHOICES = (
        ('C', 'Coach'),
        ('A', 'Administration'),
        ('P', 'Player'),
    )
    role = models.CharField(max_length=1, choices=CHOICES)


# Admin role
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    type = models.CharField(null=True, max_length=256, default=None)


# Coach role
class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    birth_date = models.DateField(default='2000-01-01')
    age = models.IntegerField(default=0)


# Player role
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    birth_date = models.DateField(default='2000-01-01')
    age = models.IntegerField(default=0)
    weight = models.CharField(null=True, max_length=256, default=None)
    height = models.CharField(null=True, max_length=256, default=None)
    number = models.IntegerField(default=0)

    @property
    def average_score(self):
        return self.mplayer.all().aggregate(Avg('score')).get('score__avg', 0.00)

    @property
    def match_count(self):
        return self.mplayer.all().aggregate(Count('score')).get('score__count', 0.00)
