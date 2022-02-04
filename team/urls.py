from django.urls import path, include
from rest_framework import routers

from apibasics.views import TeamPlayerViewSet, TeamPlayerPercentileViewSet, TeamCoachViewSet
from participant.serializer import TeamScoreSerializer
from participant.views import TeamScoresListView
from team.views import TeamListViewSet, TeamViewSet

router = routers.DefaultRouter()

urlpatterns = [

    path('', TeamListViewSet.as_view()),
    path('<int:team_id>', TeamViewSet.as_view(), name='Team view'),
    path('<int:team_id>/players', TeamPlayerViewSet.as_view(), name='Team players view'),
    path('<int:team_id>/coaches', TeamCoachViewSet.as_view(), name='Team coaches view'),
    path('<int:team_id>/percentile/<int:p>', TeamPlayerPercentileViewSet.as_view(), name='Team players percentile view'),
    path('<int:team_id>/score', TeamScoresListView.as_view(), name='Team match score view'),

]