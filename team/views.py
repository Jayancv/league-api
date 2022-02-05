from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from leagueapi import permissions
from team.models import Team
from team.serializer import TeamSerializer


class TeamListViewSet(APIView):
    permission_classes = (permissions.isAuthenticated, permissions.isAdmin,)
    serializer_class = TeamSerializer

    def get(self, request):
        """
        Get all Teams
        """
        teams = Team.objects.all()
        # for team in teams:
        #     teamAvg = 0
        #     matchCount = 0
        #     matches = MatchTeam.objects.select_related('team').filter(team_id=team.id)
        #     for match in matches:
        #         players = MatchPlayer.objects.select_related('match').filter(match_id=match.id)
        #

        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create new team
        """
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamViewSet(APIView):
    permission_classes = (permissions.isAuthenticated , permissions.isAdmin,)
    serializer_class = TeamSerializer

    def get(self, request, team_id):
        """
        Get one team
        """
        team = Team.objects.filter(id=team_id)
        serializer = TeamSerializer(team, many=True)
        if team:  # checking if queryset is empty
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, team_id):
        """
        Modify Team details
        """
        team = Team.objects.get(id=team_id)
        serializer = TeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, team_id):
        """
        Permanently delete a team
        """
        team = Team.objects.get(id=team_id)
        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

