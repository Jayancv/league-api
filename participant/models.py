from django.db import models

# Create your models here.

from game.models import Match


# A weak entity which hold the player-match relationship
class MatchPlayer(models.Model):
    player = models.ForeignKey('apibasics.Player', on_delete=models.CASCADE, related_name='mplayer')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='taken_match')
    score = models.DecimalField(decimal_places=2, max_digits=5)

    class Meta:
        unique_together = ('player', 'match')


# A weak entity which hold the Team-match relationship
class MatchTeam(models.Model):
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE, related_name='mTeam')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='team_match')
    bonus_score = models.DecimalField(decimal_places=2, max_digits=5)

    class Meta:
        unique_together = ('team', 'match')

    # @property
    # def total_score(self):
    #     return self.mplayer.all().aggregate(Sum('score')).get('score__avg', 0.00)
    #
    # @property
    # def player_score(self):
    #     return self.mplayer.all().aggregate(Count('score')).get('score__count', 0.00)
