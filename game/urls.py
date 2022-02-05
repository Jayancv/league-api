from django.urls import path, include
from rest_framework import routers

from game import views

app_name = 'game'
router = routers.DefaultRouter()

urlpatterns = [
    #
    # path('', include(router.urls)),

    path('match', views.MatchListViewSet.as_view(), name='match view'),
    path('match/<int:match_id>', views.MatchViewSet.as_view(), name='match view'),
    path('tournament', views.TournamentListViewSet.as_view(),  name='tournament view'),
    path('tournament/<int:tou_id>', views.TournamentViewSet.as_view(),  name='tournament view'),
    path('tournament/<int:tou_id>/scoreboard', views.ScoreBoardViewSet.as_view(),  name='tournament dashboard view'),

]
