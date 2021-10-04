from django.contrib import admin
from .models import LocationUser

class LocationUserAdmin(admin.ModelAdmin):
    readonly_fields = ['location_lat', 'location_long', 'location_name', 'is_finished', 'start', 'end', 'user',]


admin.site.register(LocationUser, LocationUserAdmin)
