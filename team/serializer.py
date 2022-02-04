from rest_framework import serializers

from team.models import Team


class TeamSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    match_count = serializers.IntegerField(required=False, read_only=True)
    avarege = serializers.IntegerField(read_only=True)


    def create(self, validated_data):
        team = Team.objects.create(name=validated_data['name'])
        return team

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
