from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Location

class LocationSerializer(GeoFeatureModelSerializer):
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    
    class Meta:
        model = Location
        geo_field = 'point'
        fields = ('id', 'name', 'description', 'address', 'latitude', 'longitude', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class LocationListSerializer(serializers.ModelSerializer):
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    
    class Meta:
        model = Location
        fields = ('id', 'name', 'description', 'address', 'latitude', 'longitude', 'created_at')