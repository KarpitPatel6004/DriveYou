import json
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.serializers import serialize
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.views.decorators.http import require_POST

from .models import SearchRequest
from .forms import DriverCustomAuthenticationForm, DriverRegistrationForm, SearchRequestForm, UserRegistrationForm, UserCustomAuthenticationForm, \
    CustomPasswordResetForm, CarForm

def driveyou_homescreen(request):
    return render(request, 'home.html')

def register_view_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_client = True
            user.save()
            return redirect('user_login')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def register_view_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_driver = True
            user.save()
            return redirect('driver_login')
    else:
        form = DriverRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
    

def user_login_view(request):
    if request.method == 'POST':
        form = UserCustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_client:
                login(request, user)
                return redirect('user_home_screen')
            else:
                return HttpResponseForbidden("You are not authorized to access this page.")
    else:
        form = UserCustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def driver_login_view(request):
    if request.method == 'POST':
        form = DriverCustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_driver: 
                login(request, user)
                return redirect('driver_home_screen')
            else:
                return HttpResponseForbidden("You are not authorized to access this page.")
    else:
        form = DriverCustomAuthenticationForm()

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
    accepted_requests = user.search_results.filter(accepted=True)
    pending_requests = user.search_results.filter(accepted=False)
    context = {'user': user, 'cars': cars, 
               'accepted_requests': accepted_requests, 'pending_requests': pending_requests}
    return render(request, 'user_home_screen.html', context)

@login_required(login_url="driver_login")
def driver_home_screen(request):
    driver = request.user
    driver_rides = SearchRequest.objects.filter(driver=driver)
    context = {'ride_history': driver_rides, 
               'total_earnings': driver.earnings,
               'user': driver}
    return render(request, 'driver_home_screen.html', context)

@login_required(login_url="driver_login")
def update_driver_location(request):
    if request.method == 'POST':
        driver = request.user
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        if lat is not None and lon is not None:
            driver.location_lat = lat
            driver.location_lon = lon
            # driver.location = Point(float(lon), float(lat))
            driver.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Latitude and longitude are required.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

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
            search_request.start_point = Point(float(start_lon), float(start_lat))
            search_request.save()

            # TODO: Redirect to map to show nearby drivers
            return redirect('user_home_screen')
    else:
        form = SearchRequestForm()

    return render(request, 'need_driver.html', {'form': form})

@login_required(login_url="driver_login")
def find_rides(request):
    user = request.user
    
    # TODO: Filtering the request based on distance from driver's location
    # search_requests = SearchRequest.objects.annotate(
    #     distance_from_driver=Distance(Point(('start_lon', 'start_lat'), srid=4326),
    #                                   Point((user.location_lon, user.location_lat), srid=4326))
    # ).filter(distance__lte=10)

    search_requests = SearchRequest.objects.filter(accepted=False)
    
    search_requests_json = serialize('json', search_requests)
    context = {'search_requests': search_requests_json, 'user': user}
    return render(request, 'find_rides.html', context)

@require_POST
def update_ride_status(request, ride_id):
    driver = request.user
    search_request = get_object_or_404(SearchRequest, id=ride_id)
    search_request.accepted = True
    search_request.driver = driver
    search_request.save()
    driver.earnings = driver.earnings + search_request.price
    driver.save()
    return JsonResponse({'status': 'success'})