from django.urls import path, include

from apibasics import views

app_name = 'apibasic'
urlpatterns = [
    path('auth', views.AccessTokenPairView.as_view()),
    path('users', views.UsersListView.as_view()),
    path('players', views.PlayerListView.as_view()),
    path('coaches', views.CoachListView.as_view()),
    path('players/<int:player_id>', views.PlayerView.as_view(), name='player view'),
    path('players/<int:player_id>/scores', include('participant.urls'), name='player score view'),
    path('coaches/<int:coach_id>', views.CoachView.as_view(), name='coach view'),
    path('teams/', include('team.urls'), name='team view'),
    path('game/', include('game.urls'), name='Match view'),

]