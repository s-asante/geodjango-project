from django.contrib.gis import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.GISModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'address')
    readonly_fields = ('created_at', 'updated_at', 'latitude', 'longitude')
    
    
    default_lon = 0
    default_lat = 0
    default_zoom = 2