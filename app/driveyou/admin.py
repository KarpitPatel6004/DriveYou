from django.contrib import admin
from .models import Car, Driver, SearchRequest, User

admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Car)
admin.site.register(SearchRequest)