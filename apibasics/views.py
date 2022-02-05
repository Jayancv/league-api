from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apibasics.models import Coach, Player, User, Admin
from apibasics.serializer import CoachSerializer, PlayerSerializer, GroupSerializer, PlayerWithAvg, \
    AccessTokenPairSerializer, UniqueDetailsSerializer, AdminSerializer
from leagueapi import permissions


class UsersListView(APIView):
    """
    API endpoint that allows users to be viewed or create.
    """
    permission_classes = (permissions.IsAuthenticated, permissions.isAdmin)

    def get(self, request):
        users = User.objects.all()
        serializer = UniqueDetailsSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminListView(APIView):
    """
    API endpoint that allows users to be viewed or create.
    """
    permission_classes = (permissions.IsAuthenticated, permissions.isAdmin)

    def get(self, request):
        users = Admin.objects.all()
        serializer = AdminSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        """
        Create new admin user
        """
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminView(APIView):
    """
    API endpoint that allows to be viewed or edited a admin.
    """
    permission_classes = (permissions.isAuthenticated | permissions.isAdmin,)
    serializer_class = AdminSerializer

    def get(self, request, admin_id):
        """
        Get one admin
        """
        admin = Admin.objects.filter(user_id=admin_id)
        serializer = AdminSerializer(admin, many=True)
        if admin:  # checking if queryset is empty
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, admin_id):
        """
        Modify admin details
        """
        admin = Admin.objects.get(user_id=admin_id)
        serializer = AdminSerializer(admin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, admin_id):
        """
        Permanently delete a admin and their user details
        """
        admin = Admin.objects.get(user_id=admin_id)
        user = User.objects.get(id=admin_id)
        admin.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoachListView(APIView):
    """
    API endpoint that allows coaches to be viewed or edited.
    """
    permission_classes = (permissions.isAuthenticated, permissions.isAdmin,)
    serializer_class = CoachSerializer

    def get(self, request):
        """
        Get all coaches
        """
        coaches = Coach.objects.all()
        serializer = CoachSerializer(coaches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        """
        Create new coach
        """
        serializer = CoachSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoachView(APIView):
    """
    API endpoint that allows to be viewed or edited a coach.
    """
    permission_classes = (permissions.isAuthenticated | permissions.isAdmin,)
    serializer_class = CoachSerializer

    def get(self, request, coach_id):
        """
        Get one coach
        """
        coach = Coach.objects.filter(user_id=coach_id)
        serializer = CoachSerializer(coach, many=True)
        if coach:  # checking if queryset is empty
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, coach_id):
        """
        Modify coach details
        """
        coach = Coach.objects.get(user_id=coach_id)
        serializer = CoachSerializer(coach, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, coach_id):
        """
        Permanently delete a coach and their user details
        """
        coach = Coach.objects.get(user_id=coach_id)
        user = User.objects.get(id=coach_id)
        coach.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerWithAvg
    permission_classes = [permissions.IsAuthenticated]


class PlayerListView(APIView):
    """
    API endpoint that allows Players to be viewed or create.
    """
    permission_classes = (permissions.isAuthenticated, (permissions.isCoach | permissions.isAdmin),)
    serializer_class = PlayerSerializer

    def get(self, request):
        """
        Get all Players
        """
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        """
        Create new Player
        """
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerView(APIView):
    """
    API endpoint that allows to be viewed or edit single player.
    """
    permission_classes = (permissions.isAuthenticated, permissions.isAdmin | permissions.isCoach,)
    serializer_class = PlayerSerializer

    def get(self, request, player_id):
        """
        Get one player
        """
        player = Player.objects.filter(user_id=player_id)
        serializer = PlayerSerializer(player, many=True)
        if player:  # checking if queryset is empty
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, player_id):
        """
        Modify player details
        """
        player = Player.objects.get(user_id=player_id)
        serializer = PlayerSerializer(player, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, player_id):
        """
        Permanently delete player and their user details
        """
        player = Player.objects.get(user_id=player_id)
        user = User.objects.get(id=player_id)
        player.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamPlayerViewSet(APIView):
    """
    API endpoint that allows to be viewed players in a Team.
    """
    permission_classes = (
        permissions.isAuthenticated, (permissions.isAdmin | (permissions.isCoach & permissions.isSameTeam)),)
    serializer_class = PlayerSerializer

    def get(self, request, team_id):
        """
        Get all players in the team
        """
        percentile = request.query_params.get("percentile")
        p = 0
        if percentile is not None and percentile.isnumeric():
            p = int(percentile)
        players_list = []
        players = Player.objects.select_related('team').filter(team_id=team_id).order_by('-user_id')
        team_avg = 0
        count = 1
        for player in players:
            if player.average_score is not None and player.average_score.isnumeric():
                team_avg = team_avg + player.average_score
                count = count + 1

        percentile_avg = (team_avg / count) * p / 100
        for player in players:
            if player.average_score is not None and player.average_score.isnumeric():
                if player.average_score > percentile_avg:
                    players_list.append(player)
            else:
                players_list.append(player)

        serializer = PlayerSerializer(players_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamCoachViewSet(APIView):
    """
    API endpoint that allows to be viewed coaches in a Team.
    """
    permission_classes = (permissions.isAuthenticated, permissions.isAdmin,)
    serializer_class = CoachSerializer

    def get(self, request, team_id):
        """
        Get all coaches in the given team
        """
        players_list = []
        coaches = Coach.objects.select_related('team').filter(team_id=team_id)
        for ch in coaches:
            players_list.append(ch)
        serializer = PlayerSerializer(players_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (permissions.isAuthenticated, permissions.isAdmin,)

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccessTokenPairView(TokenObtainPairView):
    """
    API endpoint that allows to generate API access token.
    """
    serializer_class = AccessTokenPairSerializer
