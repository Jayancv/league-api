# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import Tournament, Match
from game.serializer import MatchSerializer, TournamentSerializer, TournamentUpdateSerializer, MatchUpdateSerializer
from leagueapi import permissions


class TournamentListViewSet(APIView):
    """
    API endpoint that allows Tournaments to be viewed or created.
    """
    permission_classes = (permissions.IsAuthenticated, permissions.isAdmin)
    serializer_class = TournamentSerializer

    def get(self, request):
        """
        Get all Tournament details
        """
        teams = Tournament.objects.all()
        serializer = TournamentSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create new tournament
        """
        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentViewSet(APIView):
    """
    API endpoint that allows to be viewed or edited single Tournament.
    """
    permission_classes = (permissions.isAuthenticated | permissions.isAdmin,)
    serializer_class = TournamentSerializer

    def get(self, request, tou_id):
        """
        Get one Tournament details
        """
        team = Tournament.objects.filter(id=tou_id)
        serializer = TournamentSerializer(team, many=True)
        if team:  # checking if queryset is empty
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, tou_id):
        """
        Modify Tournament details
        """
        team = Tournament.objects.get(id=tou_id)
        serializer = TournamentUpdateSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tou_id):
        """
        Permanently delete Tournament details
        """
        team = Tournament.objects.get(id=tou_id)
        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MatchListViewSet(APIView):
    """
    API endpoint that allows Matches to be viewed or edited.
    """
    permission_classes = (permissions.IsAuthenticated, permissions.isAdmin)
    serializer_class = MatchSerializer

    def get(self, request):
        """
        Get all matches
        """
        teams = Match.objects.all()
        serializer = MatchSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create new Match
        """
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchViewSet(APIView):
    """
    API endpoint that allows to be viewed or edited single match.
    """
    permission_classes = (permissions.isAuthenticated, permissions.isAdmin)
    serializer_class = MatchSerializer

    def get(self, request, match_id):
        """
        Get one match
        """
        team = Match.objects.filter(id=match_id)
        serializer = MatchSerializer(team, many=True)
        if team:  # checking if queryset is empty
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, match_id):
        """
        Modify match details
        """
        team = Match.objects.get(id=match_id)
        serializer = MatchUpdateSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, match_id):
        """
        Permanently delete match
        """
        team = Match.objects.get(id=match_id)
        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
