from rest_framework import serializers

from apibasics.models import Player
from game.models import Match
from game.serializer import MatchSerializer
from participant.models import MatchPlayer, MatchTeam
from team.models import Team


class MatchPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchPlayer
        fields = '__all__'


class PlayerScoreAddSerializer(serializers.Serializer):
    match_id = serializers.IntegerField()
    player_id = serializers.IntegerField()
    score = serializers.DecimalField(max_digits=19, decimal_places=1)

    def validate_match_id(self, match_id):
        """
        Check that the match id exists
        """
        if not Match.objects.filter(id=match_id).exists():
            raise serializers.ValidationError('match id does not exist')
        return match_id

    def validate_player_id(self, player_id):
        """
        Check that the player id exists
        """
        if not Player.objects.filter(pk=player_id):
            raise serializers.ValidationError('player id does not exist')
        return player_id

    def validate(self, data):
        """
        Check that score for specified player id  and match id does not already exist
        """
        if MatchPlayer.objects.filter(player_id=data['player_id'], match_id=data['match_id']).exists():
            raise serializers.ValidationError('Selection already exists for this player in this match')
        return data

    def create(self, validated_data):
        new_score = MatchPlayer.objects.create(match_id=validated_data['match_id'],
                                               player_id=validated_data['player_id'],
                                               score=validated_data['score'])
        return new_score


class PlayerScoreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    match = MatchSerializer()
    score = serializers.DecimalField(decimal_places=1, max_digits=19)

    def update(self, instance, validated_data):
        instance.score = validated_data.get('score', instance.score)
        instance.save()
        return instance


class TeamScoreAddSerializer(serializers.Serializer):
    match_id = serializers.IntegerField()
    team_id = serializers.IntegerField()
    bonus_score = serializers.DecimalField(max_digits=5, decimal_places=2)

    def validate_match_id(self, match_id):
        """
        Check that the match id exists
        """
        if not Match.objects.filter(id=match_id).exists():
            raise serializers.ValidationError('match id does not exist')
        return match_id

    def validate_team_id(self, team_id):
        """
        Check that the Team id exists
        """
        if not Team.objects.filter(pk=team_id):
            raise serializers.ValidationError('Team id does not exist')
        return team_id

    def validate(self, data):
        """
        Check that scores for specified team and the match does not already exist
        """
        if MatchTeam.objects.filter(team_id=data['team_id'], match_id=data['match_id']).exists():
            raise serializers.ValidationError('already Added for team to this match')
        return data

    def create(self, validated_data):
        new_score = MatchTeam.objects.create(match_id=validated_data['match_id'],
                                             team_id=validated_data['team_id'],
                                             bonus_score=validated_data['bonus_score'])
        return new_score


class TeamScoreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    match = MatchSerializer()
    bonus_score = serializers.DecimalField(decimal_places=2, max_digits=5)

    def update(self, instance, validated_data):
        instance.bonus_score = validated_data.get('bonus_score', instance.bonus_score)
        instance.save()
        return instance
