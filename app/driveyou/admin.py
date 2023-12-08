from django.contrib import admin
from .models import Car, SearchRequest, User

admin.site.register(User)
admin.site.register(Car)
admin.site.register(SearchRequest)