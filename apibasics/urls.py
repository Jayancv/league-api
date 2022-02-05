from django.urls import path, include

from apibasics import views

app_name = 'apibasic'
urlpatterns = [
    path('auth', views.AccessTokenPairView.as_view()),    # To get authentication token
    path('users', views.UsersListView.as_view()),         # To get/create Users
    path('admins', views.AdminListView.as_view()),        # To get/create Admin users
    path('players', views.PlayerListView.as_view()),      # To get/create players
    path('coaches', views.CoachListView.as_view()),       # To get/create coaches
    path('admins/<int:admin_id>', views.AdminView.as_view(), name='admin view'),      # To get/update a Admin user
    path('players/<int:player_id>', views.PlayerView.as_view(), name='player view'),  # To get/update a player
    path('coaches/<int:coach_id>', views.CoachView.as_view(), name='coach view'),     # To get/update a coach

    # path('players/<int:player_id>/scores', include('participant.urls'), name='player score view'),
    path('scores/', include('participant.urls'), name='player score view'),
    path('teams/', include('team.urls'), name='team view'),
    path('games/', include('game.urls'), name='Match view'),
]