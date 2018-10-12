from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate, login


class AddUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        ''' Creates user instances '''
        password = validated_data.pop('password')
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True}
        }
    
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.logged_in = False
        self.user = None
        context = kwargs.get('context', None)
        if context:
            self.request = context['request']
    
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            self.logged_in = True
            self.user = user
        return self
    
    @property
    def data(self):
        if self.logged_in:
            data = {
                "message": "Logged In",
                'id': self.user.id
            }
        else:
            data = {
                "message": "Something went wrong"
            }
        return data

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'full_name')
    
    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
    
