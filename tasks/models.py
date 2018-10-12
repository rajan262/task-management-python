from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Team(models.Model):
    ''' Model for Team '''
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    members = models.ManyToManyField(get_user_model(), related_name='team_member')

    def __str__(self):
        return self.name

class Task(models.Model):
    ''' Model for tasks created by Admin '''
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2
    COMPLETED = 3

    STATUS_CHOICES = (
        (TODO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (COMPLETED, 'Completed'),
    )

    assigned_to = models.ForeignKey(get_user_model(), blank=True, null=True, related_name='task_user')
    team = models.ForeignKey(Team, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    deadline = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name