from django.contrib import admin

# Register your models here.
from .models import Airport, Flight, Passenger, Profile

admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Profile)

