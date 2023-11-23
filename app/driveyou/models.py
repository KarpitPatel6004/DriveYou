from django.db import models
from django.contrib.auth.models import AbstractUser
from validators import validate_mobile_number

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, validators=[validate_mobile_number])
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        app_label = 'driveyou'