from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import DriverRegistrationForm, SearchRequestForm, UserRegistrationForm, CustomAuthenticationForm, \
    CustomPasswordResetForm, CarForm

def register_view_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('user_login')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def register_view_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('driver_login')
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

@login_required(login_url="user_login")
def user_home_screen(request):
    user = request.user
    cars = user.cars.all()
    search_requests = user.search_results.all()
    return render(request, 'user_home_screen.html', {'user': user, 'cars': cars, 'search_requests': search_requests})

@login_required(login_url="driver_login")
def driver_home_screen(request):
    return render(request, 'driver_home_screen.html')

@login_required(login_url="user_login")
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()

            return redirect('user_home_screen')
    else:
        form = CarForm()

    return render(request, 'add_car.html', {'form': form})

@login_required(login_url="user_login")
def need_driver(request):
    if request.method == 'POST':
        form = SearchRequestForm(request.POST)
        start_loc = request.POST.get('start_location')
        destination = request.POST.get('destination')
        distance = request.POST.get('distance')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        start_lat = request.POST.get('start_lat')
        start_lon = request.POST.get('start_lon')
        end_lat = request.POST.get('end_lat')
        end_lon = request.POST.get('end_lon')
        if form.is_valid():
            search_request = form.save(commit=False)
            search_request.user = request.user
            search_request.start_location = start_loc
            search_request.destination = destination
            search_request.distance = distance
            search_request.duration = duration
            search_request.price = price
            search_request.start_lat = start_lat
            search_request.start_lon = start_lon
            search_request.end_lat = end_lat
            search_request.end_lon = end_lon
            search_request.save()

            # TODO: Redirect to map to show nearby drivers
            return redirect('user_home_screen')
    else:
        form = SearchRequestForm()

    return render(request, 'need_driver.html', {'form': form})
