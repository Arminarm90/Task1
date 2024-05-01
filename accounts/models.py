from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = None
    
    phone_number = models.CharField(max_length=20,unique=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    phone_number_token = models.CharField(max_length=100,null=True,blank=True)
    forget_password = models.CharField(max_length=100, null=True,blank=True)
    last_login_time = models.DateTimeField(null=True,blank=True)
    last_logout_time = models.DateTimeField(null=True,blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []