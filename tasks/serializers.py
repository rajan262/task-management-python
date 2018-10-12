from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Task, Team

class TeamSerializer(serializers.ModelSerializer):
    ''' Serializer for Team model '''

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'members',)

class TeamListSerializer(TeamSerializer):
    ''' Serializer to list users '''
    members = UserSerializer(many=True)

class UpdateCreateTaskSerializer(serializers.ModelSerializer):
    ''' Serialzer to update or create Tasks '''
    class Meta:
        model = Task
        fields = ('id', 'assigned_to', 'team', 'name', 'description', 'status', 'deadline', 'created')


class TaskSerializer(UpdateCreateTaskSerializer):
    ''' Serializer for tasks model '''
    assigned_to = UserSerializer(many=False)
    team = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'assigned_to', 'team', 'name', 'description', 'status', 'deadline', 'created')
    
    def get_team(self, obj):
       return obj.name
    
    def update(self, instance, validated_data):
        instance = Task.objects.filter(id=instance.id).update(**validated_data)
        return instance

class RetrieveDeleteSerializer(UpdateCreateTaskSerializer):
    ''' Serializer for tasks model '''
    assigned_to = UserSerializer(many=False)

    class Meta:
        model = Task
        fields = ('id', 'assigned_to', 'team', 'name', 'description', 'status', 'deadline', 'created')

    
