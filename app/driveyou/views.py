from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import DriverRegistrationForm, UserRegistrationForm, CustomAuthenticationForm, CustomPasswordResetForm

def register_view_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def register_view_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = DriverRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
    

def user_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_home_screen')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def driver_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            driver = form.get_user()
            login(request, driver)
            return redirect('driver_home_screen')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def user_logout_view(request):
    logout(request)
    return redirect('user_login')

def driver_logout_view(request):
    logout(request)
    return redirect('driver_login')

def password_reset_view(request):
    # Customize this view if needed
    pass

def user_home_screen(request):
    return render(request, 'user_home_screen.html')

def driver_home_screen(request):
    return render(request, 'driver_home_screen.html')