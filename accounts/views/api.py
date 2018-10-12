from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import AddUserSerializer, LoginSerializer, UserSerializer

class AddUser(generics.CreateAPIView):
    serializer_class = AddUserSerializer
    permission_classes = (IsAuthenticated, )

class UserLogin(generics.CreateAPIView):
    serializer_class = LoginSerializer
    queryset = get_user_model().objects.all()

class ListUser(generics.ListAPIView):
    model = get_user_model()
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = get_user_model().objects.exclude(is_staff=True)
        return queryset
    


