"""leagueapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apibasics import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'coach', views.CoachViewSet)
# router.register(r'player', views.PlayerViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/auth', apibasics.views.MyTokenObtainPairView.as_view()),
    # path('api/usersList', apibasics.views.UsersListView.as_view()),
    # path('api/playerList', apibasics.views.PlayerListView.as_view()),
    # path('api/playerList', apibasics.views.CoachListView.as_view()),

    path('', include(router.urls)),
    path('api/', include('apibasics.urls')),
    # path('participant/', include('participant.urls', namespace='participant')),
    # path('game/', include('game.urls')),
    # path('scoreboard/', include('game.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
