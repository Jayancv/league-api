from rest_framework import routers

from participant import views
from django.urls import path, include

from participant.views import PlayerScoresListView, TeamScoresListView, PlayersScoreListView, TeamsScoreListView

app_name = 'participant'
router = routers.DefaultRouter()

urlpatterns = [

    path('players', PlayersScoreListView.as_view()),
    path('players/<int:player_id>', PlayerScoresListView.as_view()),
    path('teams', TeamsScoreListView.as_view()),
    path('teams/<int:team_id>', TeamScoresListView.as_view()),

]
