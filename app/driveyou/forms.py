from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import SearchRequest, User, Car

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'email', 'name']

class DriverRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'email', 'name']

class UserCustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class DriverCustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class CustomPasswordResetForm(PasswordResetForm):
    pass

class CarForm(forms.ModelForm):
    registration_date = forms.DateField(
        label='Registration Date',
        widget=forms.widgets.DateInput(attrs={'type':'date'})
    )
    registration_expiry_date = forms.DateField(
        label='Registration Expiry Date',
        widget=forms.widgets.DateInput(attrs={'type':'date'})
    )
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'has_insurance', 'registration_number', 
                  'registration_date', 'registration_expiry_date', 'license_plate']
        
class SearchRequestForm(forms.ModelForm):
    user_travel_time = forms.SplitDateTimeField(
        label='Travel Time',
        widget=forms.widgets.SplitDateTimeWidget(date_attrs={'type':'date'}, time_attrs={'type':'time'})
    )
    class Meta:
        model = SearchRequest
        fields = ['user_travel_time']
