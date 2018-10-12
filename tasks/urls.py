from django.conf.urls import url

from .views import AdminTaskList, RetrieveDeleteTask, UpdateTask, UserTaskList, CreateTask, TaskStatistics, UserTaskStatistics, AddTeam, ListTeams

app_name = 'tasks'
urlpatterns = [
    url('^add-team/$', AddTeam.as_view(), name='add_team'),
    url('^team-list/$', ListTeams.as_view(), name='list_teams'),
    url(r'^task-list/$', AdminTaskList.as_view(), name='admin_task_list'),
    url(r'^retrieve-delete-task/$', RetrieveDeleteTask.as_view(), name='retrieve_delete_task'),
    url(r'^create-task/$', CreateTask.as_view(), name='create_task'),
    url(r'^update-task/$', UpdateTask.as_view(), name='update_task'),
    url(r'^user-task-list/$', UserTaskList.as_view(), name='user_task_list'),
    url(r'^task-statistics/$', TaskStatistics.as_view(), name='task_statistics'),
    url(r'^user-task-statistics', UserTaskStatistics.as_view(), name='user_task_statistics'),
]