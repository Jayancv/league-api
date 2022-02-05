from rest_framework import serializers

from game.models import Match, Tournament


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class TournamentSerializerModal(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class TournamentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    code = serializers.CharField(required=True)
    description = serializers.CharField()
    from_date = serializers.DateField(required=True)
    to_date = serializers.DateField(required=True)

    def create(self, validated_data):
        new_mark = Tournament.objects.create(name=validated_data['name'],
                                             code=validated_data['code'],
                                             description=validated_data['description'],
                                             from_date=validated_data['from_date'],
                                             to_date=validated_data['to_date'])
        return new_mark


class TournamentUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    code = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.description = validated_data.get('description', instance.description)
        instance.from_date = validated_data.get('from_date', instance.from_date)
        instance.to_date = validated_data.get('to_date', instance.to_date)
        instance.save()
        return instance


class MatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    from_date = serializers.DateField(required=True)
    to_date = serializers.DateField(required=True)
    tournament_id = serializers.IntegerField(required=True)
    level = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    teamA_id = serializers.IntegerField(required=True)
    teamB_id = serializers.IntegerField(required=True)
    winner_id = serializers.IntegerField(required=False, allow_null=True)
    teamA_score = serializers.DecimalField(read_only=True,required=False, max_digits=10, decimal_places=4)

    def create(self, validated_data):
        new_mark = Match.objects.create(name=validated_data['name'],
                                        tournament_id=validated_data['tournament_id'],
                                        teamA_id=validated_data['teamA_id'],
                                        teamB_id=validated_data['teamB_id'],
                                        winner_id=validated_data['winner_id'],
                                        from_date=validated_data['from_date'],
                                        to_date=validated_data['to_date'],
                                        level=validated_data['level'],
                                        status=validated_data['status'],

                                        )
        return new_mark


class MatchUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
    tournament_id = serializers.IntegerField(required=False)
    level = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    teamA_id = serializers.IntegerField(required=False)
    teamB_id = serializers.IntegerField(required=False)
    winner_id = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.from_date = validated_data.get('from_date', instance.from_date)
        instance.to_date = validated_data.get('to_date', instance.to_date)
        instance.tournament_id = validated_data.get('tournament_id', instance.tournament_id)
        instance.level = validated_data.get('level', instance.level)
        instance.status = validated_data.get('status', instance.status)
        instance.teamA_id = validated_data.get('teamA_id', instance.teamA_id)
        instance.teamB_id = validated_data.get('teamB_id', instance.teamB_id)
        instance.winner_id = validated_data.get('winner_id', instance.winner_id)
        instance.save()
        return instance

# class ScoreBoardSerializer(serializers.Serializer):
#     match_detail = MatchSerializer(source='match')
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     code = serializers.CharField(required=True)
#     description = serializers.CharField()
#     from_date = serializers.DateField(required=True)
#     to_date = serializers.DateField(required=True)