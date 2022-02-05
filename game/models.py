from django.db import models

# Create your models here.

# The highest level of the game
from django.db.models import Sum


class Tournament(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=2000, null=True)
    from_date = models.DateField(default='2022-01-01')
    to_date = models.DateField(default='2022-05-31')


# Single match in the tournament
class Match(models.Model):
    name = models.CharField(max_length=255)
    from_date = models.DateField(default='2022-01-01')
    to_date = models.DateField(default='2022-01-01')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    LEVEL = (
        ('1', 'Entry'),  # 16 Teams
        ('2', 'Selection'),  # 8 teams
        ('3', 'Semi'),  # 4 teams
        ('4', 'Final'),  # 2 teams
    )
    level = models.CharField(max_length=1, choices=LEVEL, default='1')
    STATUS = (
        ('0', 'Pending'),  # Planning stage
        ('1', 'Ongoing'),  # Currently match stated
        ('2', 'Complete'),  # Match completed successfully
        ('3', 'Abandoned'),  # Match was not held
    )
    status = models.CharField(max_length=1, choices=STATUS, default='0')
    teamA = models.ForeignKey('team.Team', on_delete=models.CASCADE, related_name='teamA', null=True)
    teamB = models.ForeignKey('team.Team', on_delete=models.CASCADE, related_name='teamB', null=True)
    winner = models.ForeignKey('team.Team', on_delete=models.CASCADE, related_name='winner', null=True)

    @property
    def teamA_score(self):
        player_score = 0
        team_score = self.team_match.all().filter(team=self.teamA).aggregate(Sum('bonus_score')).get('bonus_score__sum', 0.00)
        players_list = self.taken_match.select_related('player').filter(match_id=self.id,
                                                                       player__team_id=self.teamA.id).all()
        for player in players_list:
            player_score = player_score + player.score

        if team_score is not None:
            player_score = player_score + int(team_score)
        return player_score

    @property
    def teamB_score(self):
        player_score = 0
        team_score = self.team_match.all().filter(team=self.teamB).aggregate(Sum('bonus_score')).get('bonus_score__sum',
                                                                                                     0.00)
        players_list = self.taken_match.select_related('player').filter(match_id=self.id,
                                                                       player__team_id=self.teamB.id).all()
        for player in players_list:
            player_score = player_score + player.score

        if team_score is not None:
            player_score = player_score + int(team_score)
        return player_score
