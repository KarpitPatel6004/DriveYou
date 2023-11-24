from django.contrib import admin
from .models import Driver, User

admin.site.register(User)
admin.site.register(Driver)