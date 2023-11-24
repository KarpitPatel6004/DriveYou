from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import Driver, SearchRequest, User, Car

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

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'has_insurance', 'registration_number', 
                  'registration_date', 'registration_expiry_date', 'license_plate']
        
class SearchRequestForm(forms.ModelForm):
    class Meta:
        model = SearchRequest
        fields = ['start_location', 'destination', 'user_travel_time']
