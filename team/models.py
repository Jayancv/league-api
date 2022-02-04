from django.db import models

# Create your models here.
from django.db.models import Count, Avg


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)

    # @property
    # def average_score(self):
    #     teamAvg = self.mTeam.all().aggregate(Avg('bonus_score')).get('bonus_score__avg', 0.00)
    #     playerAvg =
    #     return self.mTeam.all().aggregate(Avg('bonus_score')).get('bonus_score__avg', 0.00)

    @property
    def match_count(self):
        return self.mTeam.all().aggregate(Count('bonus_score')).get('bonus_score__count', 0.00)