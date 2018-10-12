from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    '''
    User Custom Manager
    '''

    def create_user(self, email=None, password=None):
        '''
        Create User
        '''
        if not email:
            raise ValueError('User must have a email address')
        user = self.model(email=self.normalize_email(email))
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        '''
        Create Superuser
        '''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
class User(AbstractBaseUser, PermissionsMixin,):
    '''
    If no need to use UserGroups/Permissions then remove PermissionsMixin
    '''
    email = models.EmailField('Email Address', unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField('Staff member', default=False)
    is_active = models.BooleanField('Active', default=True)
    is_superuser = models.BooleanField('Is a Super user', default=False)
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return '{0}'.format(self.first_name, )

    USERNAME_FIELD = 'email'

    class Meta(object):
        ''' User Class Meta '''
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        app_label = 'accounts'





