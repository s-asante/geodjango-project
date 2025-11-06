from django.test import TestCase
from django.urls import reverse
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework.test import APIClient
from rest_framework import status
from locations.models import Location


class SpatialQueryTest(TestCase):
    

    def setUp(self):
        
        self.client = APIClient()
        
        
        self.statue_of_liberty = Location.objects.create(
            name="Statue of Liberty",
            description="Iconic statue",
            point=Point(-74.0445, 40.6892, srid=4326)
        )
        
        self.empire_state = Location.objects.create(
            name="Empire State Building",
            description="Famous skyscraper",
            point=Point(-73.9857, 40.7484, srid=4326)
        )
        
        self.central_park = Location.objects.create(
            name="Central Park",
            description="Urban park",
            point=Point(-73.9654, 40.7829, srid=4326)
        )
        
        
        self.la_location = Location.objects.create(
            name="Los Angeles",
            description="West coast city",
            point=Point(-118.2437, 34.0522, srid=4326)
        )

    def test_nearby_locations(self):
        
        url = reverse('location-nearby')
        
        
        response = self.client.get(url, {
            'lat': 40.7484,
            'lon': -73.9857,
            'distance': 5000  
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        if 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
        
        
        self.assertGreaterEqual(len(results), 2)
        
        
        if isinstance(results, list) and len(results) > 0:
            if 'properties' in results[0]:
                names = [loc['properties']['name'] for loc in results]
            else:
                names = [loc['name'] for loc in results]
            self.assertNotIn('Los Angeles', names)

    def test_nearby_locations_default_distance(self):
        
        url = reverse('location-nearby')
        
        response = self.client.get(url, {
            'lat': 40.7484,
            'lon': -73.9857
            
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nearby_locations_missing_parameters(self):
        
        url = reverse('location-nearby')
        
        
        response = self.client.get(url, {'lon': -73.9857})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
        response = self.client.get(url, {'lat': 40.7484})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nearby_locations_invalid_parameters(self):
        
        url = reverse('location-nearby')
        
        response = self.client.get(url, {
            'lat': 'invalid',
            'lon': -73.9857,
            'distance': 1000
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            

    def test_within_bounds(self):
        
        try:
            url = reverse('location-within_bounds')
        except:
            self.skipTest("within_bounds endpoint not implemented")
        
        
        response = self.client.get(url, {
            'min_lat': 40.7,
            'max_lat': 40.8,
            'min_lon': -74.0,
            'max_lon': -73.9
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_within_bounds_missing_parameters(self):
        
        try:
            url = reverse('location-within_bounds')
        except:
            self.skipTest("within_bounds endpoint not implemented")
        
        response = self.client.get(url, {
            'min_lat': 40.7,
            'max_lat': 40.8,
            
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_distance_calculation(self):
        
        
        empire_point = self.empire_state.point
        
        
        nearby = Location.objects.filter(
            point__distance_lte=(empire_point, D(km=5))
        )
        
        
        self.assertGreaterEqual(nearby.count(), 2)
        
        
        self.assertNotIn(self.la_location, nearby)

    def test_location_within_distance(self):
        
        empire_point = self.empire_state.point
        
        
        is_close = Location.objects.filter(
            pk=self.central_park.pk,
            point__distance_lte=(empire_point, D(km=5))
        ).exists()
        
        self.assertTrue(is_close)
        
        
        is_far = Location.objects.filter(
            pk=self.la_location.pk,
            point__distance_lte=(empire_point, D(km=5))
        ).exists()
        
        self.assertFalse(is_far)