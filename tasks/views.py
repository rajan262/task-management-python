from django.shortcuts import render
from django.db.models import When, IntegerField, Sum, Case, Count
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TaskSerializer, UpdateCreateTaskSerializer, TeamSerializer, TeamListSerializer, RetrieveDeleteSerializer
from .models import Task, Team

# Create your views here.
class AddTeam(generics.CreateAPIView):
    serializer_class = TeamSerializer

class ListTeams(generics.ListAPIView):
    serializer_class = TeamListSerializer
    queryset = Team.objects.all().order_by('id');

class AdminTaskList(generics.ListAPIView):
    ''' Returns list of tasks '''
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        kwargs['team_name'] = True
        return super(AdminTaskList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.all().order_by('status')

class RetrieveDeleteTask(generics.RetrieveDestroyAPIView):
    serializer_class = RetrieveDeleteSerializer

    def get(self, request, *args, **kwargs):
        kwargs['team_name'] = False
        return super(RetrieveDeleteTask, self).get(request, *args, **kwargs)

    def get_object(self):
        task_id = self.request.query_params['id']
        obj = Task.objects.filter(id=task_id).first()
        return obj

class UpdateTask(generics.UpdateAPIView):
    ''' Updates a task values '''
    serializer_class = UpdateCreateTaskSerializer

    def get_object(self):
        task_id = self.request.data['id']
        return Task.objects.filter(id=task_id).first()
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        user_id = self.request.data.pop('assigned_to')['id']
        self.request.data['assigned_to'] = user_id
        return super(UpdateTask, self).update(request, *args, **kwargs)

class CreateTask(generics.CreateAPIView):
    ''' View to create tasks by Admin '''
    serializer_class = UpdateCreateTaskSerializer

class TaskStatistics(APIView):
    ''' Returns task statistics '''
    def get(self, request, *args, **kwargs):
        response = {}
        task_queryset = Task.objects.all()
        total_tasks = task_queryset.count()
        response['total_tasks'] = total_tasks
        response['todo_tasks_percent'] = task_queryset.filter(status=Task.TODO).count()/total_tasks;
        response['in_progress_tasks_percent'] = task_queryset.filter(status=Task.IN_PROGRESS).count()/total_tasks;
        response['done_tasks_percent'] = task_queryset.filter(status=Task.DONE).count()/total_tasks;
        response['completed_tasks_percent'] = task_queryset.filter(status=Task.COMPLETED).count()/total_tasks;
        return Response(response)

class UserTaskStatistics(APIView):
    ''' Returns user tasks statistics '''
    def get(self, request, *args, **kwargs):
        response = {}
        responses = Task.objects.values('assigned_to').annotate(
            total_tasks_assigned=Count('id'),
            tasks_to_do=Sum(Case(When(status=Task.TODO, then=1), output_field=IntegerField())),
            tasks_in_progress=Sum(Case(When(status=Task.IN_PROGRESS, then=1), output_field=IntegerField())),
            tasks_done=Sum(Case(When(status=Task.DONE, then=1), output_field=IntegerField())),
            tasks_completed=Sum(Case(When(status=Task.COMPLETED, then=1), output_field=IntegerField()))
        )
        for response in responses:
            response['assigned_to'] = get_user_model().objects.get(id=response['assigned_to']).get_full_name()
        return Response(responses)


class UserTaskList(generics.ListAPIView):
    ''' Tasks list for non-admin users '''
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        kwargs['team_name'] = True
        return super(UserTaskList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        user_id = self.request.query_params['user_id']
        return Task.objects.filter(assigned_to_id=user_id).exclude(status=Task.COMPLETED).order_by('status')

