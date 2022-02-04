from rest_framework import routers

from participant import views
from django.urls import path, include

from participant.views import PlayerScoresListView

app_name = 'participant'
router = routers.DefaultRouter()

urlpatterns = [

    path('', PlayerScoresListView.as_view()),
]
