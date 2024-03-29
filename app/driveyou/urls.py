"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import driver_home_screen, driver_login_view, driveyou_homescreen, find_rides, register_view_driver, register_view_user, update_driver_location, update_ride_status, \
    user_login_view, user_logout_view, password_reset_view, user_home_screen, driver_logout_view, \
    add_car, need_driver

urlpatterns = [
    path('', driveyou_homescreen, name='home'),
    path('user_register/', register_view_user, name='user_register'),
    path('driver_register/', register_view_driver, name='driver_register'),
    path('user_login/', user_login_view, name='user_login'),
    path('driver_login/', driver_login_view, name='driver_login'),
    path('user_logout/', user_logout_view, name='user_logout'),
    path('driver_logout/', driver_logout_view, name='driver_logout'),
    # path('password_reset/', password_reset_view, name='password_reset'),
    path('user_home_screen/', user_home_screen, name='user_home_screen'),
    path('driver_home_screen/', driver_home_screen, name='driver_home_screen'),
    path('add_car/', add_car, name='add_car'),
    path('need_driver/', need_driver, name='need_driver'),
    path('find_rides/', find_rides, name='find_rides'),
    path('update_driver_location/', update_driver_location, name='update_driver_location'),
    path('update-ride-status/<int:ride_id>/', update_ride_status, name='update_ride_status'),
]
