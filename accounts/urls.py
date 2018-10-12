from django.conf.urls import url
from .views.api import UserLogin, ListUser, AddUser

urlpatterns = [
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^add-user/$', AddUser.as_view(), name='add_user'),
    url(r'^list-user/$', ListUser.as_view(), name='list_user'),
]