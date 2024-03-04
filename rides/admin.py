from django.contrib import admin
from rides.models import Route, RideRequest, Ride

# Register your models here.
admin.site.register(Route, admin.ModelAdmin)
admin.site.register(RideRequest, admin.ModelAdmin)
admin.site.register(Ride, admin.ModelAdmin)