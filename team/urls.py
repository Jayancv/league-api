from django.urls import path, include, re_path
from rest_framework import routers

from apibasics.views import TeamPlayerViewSet, TeamCoachViewSet
from team.views import TeamListViewSet, TeamViewSet

router = routers.DefaultRouter()

urlpatterns = [

    path('', TeamListViewSet.as_view()),
    path('<int:team_id>', TeamViewSet.as_view(), name='Team view'),
    path('<int:team_id>/players/', TeamPlayerViewSet.as_view(), name='Team players view'),
    path('<int:team_id>/players/(?P<percentile>\d+)', TeamPlayerViewSet.as_view(), name='Team players by percentile'),
    path('<int:team_id>/coaches', TeamCoachViewSet.as_view(), name='Team coaches view'),

]
