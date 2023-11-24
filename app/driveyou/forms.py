from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import Driver, User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'email', 'name']

class DriverRegistrationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ['phone', 'email', 'name']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class CustomPasswordResetForm(PasswordResetForm):
    pass

