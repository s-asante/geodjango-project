from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from .models import Location
from .serializers import LocationSerializer, LocationListSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return LocationListSerializer
        return LocationSerializer

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """
        Find locations within a certain distance of a point.
        
        Query Parameters:
        - lat: Latitude (required)
        - lon: Longitude (required)
        - distance: Distance in meters (default: 1000)
        
        Example: /api/locations/nearby/?lat=40.7128&lon=-74.0060&distance=5000
        """
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        distance = request.query_params.get('distance', 1000)

        if not lat or not lon:
            return Response(
                {'error': 'Both lat and lon parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(lat)
            lon = float(lon)
            distance = float(distance)
        except ValueError:
            return Response(
                {'error': 'Invalid parameter values'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_point = Point(lon, lat, srid=4326)
        
        nearby_locations = Location.objects.filter(
            point__distance_lte=(user_point, D(m=distance))
        ).annotate(
            distance=Distance('point', user_point)
        ).order_by('distance')

        serializer = self.get_serializer(nearby_locations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def within_bounds(self, request):
        """
        Find locations within a bounding box.
        
        Query Parameters:
        - min_lat, max_lat, min_lon, max_lon (all required)
        
        Example: /api/locations/within_bounds/?min_lat=40.7&max_lat=40.8&min_lon=-74.1&max_lon=-74.0
        """
        try:
            min_lat = float(request.query_params.get('min_lat'))
            max_lat = float(request.query_params.get('max_lat'))
            min_lon = float(request.query_params.get('min_lon'))
            max_lon = float(request.query_params.get('max_lon'))
        except (TypeError, ValueError):
            return Response(
                {'error': 'All bounding box parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        locations = Location.objects.filter(
            point__latitude__gte=min_lat,
            point__latitude__lte=max_lat,
            point__longitude__gte=min_lon,
            point__longitude__lte=max_lon,
        )

        serializer = self.get_serializer(locations, many=True)
        return Response(serializer.data)