from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apibasics.models import User, Coach, Player, Admin
from game.serializer import MatchSerializer
from team.models import Team


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def validate_username(self, username):
        found = False
        for i in User.objects.all():
            if username == i.username:
                found = True
                break
        if found:
            raise serializers.ValidationError('username already exists.')
        return username


class UniqueDetailsSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    email = serializers.EmailField()


class CoachSerializer(serializers.Serializer):
    user_details = UserSerializer(source='user')

    birth_date = serializers.DateField(required=False, allow_null=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    team_id = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data['user'])
        coach = Coach.objects.create(user_id=new_user.id,
                                     birth_date=validated_data['birth_date'],
                                     age=validated_data['age'],
                                     team_id=validated_data['team_id'], )

        user_group = Group.objects.get(name='coach')
        new_user.groups.add(user_group)
        return coach

    def update(self, instance, validated_data):
        user_details = validated_data.pop('user', None)
        coach_details = validated_data

        if user_details is not None:
            user = User.objects.get(id=instance.user_id)
            user.username = user_details.get('username', user.username)
            user.set_password(user_details.get('password', user.password))
            user.first_name = user_details.get('first_name', user.first_name)
            user.last_name = user_details.get('last_name', user.last_name)
            user.email = user_details.get('email', user.email)
            user.save()

        if coach_details is not None:
            instance.age = validated_data.get('age', instance.age)
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.team_id = validated_data.get('team_id', instance.team_id)
            instance.save()

        return instance


class PlayerSerializer(serializers.Serializer):
    user_details = UserSerializer(source='user')

    birth_date = serializers.DateField(required=False)
    age = serializers.IntegerField(required=False)
    weight = serializers.CharField(required=False, allow_null=True)
    height = serializers.CharField(required=False, allow_null=True)
    team_id = serializers.IntegerField(required=False)
    number = serializers.IntegerField(required=False)
    average_score = serializers.DecimalField(required=False, max_digits=10, decimal_places=4, read_only=True)
    match_count = serializers.IntegerField(required=False, read_only=True)

    def validate_team_id(self, team_id):
        """
        Check that the team id exists
        """
        if not Team.objects.filter(pk=team_id):
            raise serializers.ValidationError('team id does not exist')
        return team_id

    def create(self, validated_data):

        new_user = User.objects.create_user(**validated_data['user'])
        player = Player.objects.create(user_id=new_user.id,
                                       birth_date=validated_data['birth_date'],
                                       age=validated_data['age'],
                                       weight=validated_data['weight'],
                                       height=validated_data['height'],
                                       team_id=validated_data['team_id'],
                                       number=validated_data['number'], )

        user_group = Group.objects.get(name='player')
        new_user.groups.add(user_group)
        return player

    def update(self, instance, validated_data):
        user_details = validated_data.pop('user', None)
        player_details = validated_data

        if user_details is not None:
            user = User.objects.get(id=instance.user_id)
            user.username = user_details.get('username', user.username)
            user.set_password(user_details.get('password', user.password))
            user.first_name = user_details.get('first_name', user.first_name)
            user.last_name = user_details.get('last_name', user.last_name)
            user.email = user_details.get('email', user.email)
            user.save()

        if player_details is not None:
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.age = validated_data.get('age', instance.age)
            instance.number = validated_data.get('number', instance.number)
            instance.weight = validated_data.get('weight', instance.weight)
            instance.height = validated_data.get('height', instance.height)
            instance.team_id = validated_data.get('team_id', instance.team_id)
            instance.save()

        return instance

class PlayerBasicSerializer(serializers.Serializer):
    user_details = UniqueDetailsSerializer(source='user')


class AdminSerializer(serializers.Serializer):
    user_details = UserSerializer(source='user')
    type = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        new_user = User.objects.create_superuser(**validated_data['user'])
        user_group = Group.objects.get(name='admin')
        new_user.groups.add(user_group)
        admin = Admin.objects.create(user_id=new_user.id,
                                     type=validated_data['type'], )
        return admin

    def update(self, instance, validated_data):
        user_details = validated_data.pop('user', None)
        admin_details = validated_data

        if user_details is not None:
            user = User.objects.get(id=instance.user_id)
            user.username = user_details.get('username', user.username)
            user.set_password(user_details.get('password', user.password))
            user.first_name = user_details.get('first_name', user.first_name)
            user.last_name = user_details.get('last_name', user.last_name)
            user.email = user_details.get('email', user.email)
            user.save()

        if admin_details is not None:
            instance.birth_date = validated_data.get('type', instance.type)
            instance.save()

        return instance


class PlayerWithAvg(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating

    class Meta:
        model = Player
        fields = ['id', 'age', 'average_rating']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AccessTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        roles = []
        groups = user.groups.all()

        for group in groups:
            roles.append(group.name)

        token['roles'] = roles
        return token
