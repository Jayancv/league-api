# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from leagueapi import permissions
from participant.models import MatchPlayer, MatchTeam
from participant.serializer import MatchPlayerSerializer, PlayerScoreSerializer, PlayerScoreAddSerializer, \
    TeamScoreSerializer, TeamScoreAddSerializer


class MatchPlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows match players to be viewed or edited.
    """
    queryset = MatchPlayer.objects.all()
    serializer_class = MatchPlayerSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlayerScoresListView(APIView):
    """
    API endpoint that allows match players to be viewed or create.
    Can use to add players to match
    """
    permission_classes = (
        permissions.isAuthenticated, permissions.isAdmin | (permissions.isCoach | permissions.isSameTeam,))

    def get(self, request, player_id):
        """
        Get a list of players with there scores in each match
        """
        matches_list = []
        matches = MatchPlayer.objects.select_related('match').filter(player_id=player_id)
        for mch in matches:
            matches_list.append(mch)
        serializer = PlayerScoreSerializer(matches_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, player_id):
        """
        Adding a player to a match
        """
        serializer = PlayerScoreAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'player assigned successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamScoresListView(APIView):
    """
    API endpoint that allows match playing teams to be viewed or create.
    Can use to add teams to match
    """
    permission_classes = (
        permissions.isAuthenticated, permissions.isAdmin | (permissions.isCoach | permissions.isSameTeam,))

    def get(self, request, team_id):
        """
        Get a list matches scores with a team
        """
        matches_list = []
        matches = MatchTeam.objects.select_related('match').filter(team_id=team_id)
        for mch in matches:
            matches_list.append(mch)
        serializer = TeamScoreSerializer(matches_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, team_id):
        """
        Assign a team to a match
        """
        serializer = TeamScoreAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Team assigned successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
