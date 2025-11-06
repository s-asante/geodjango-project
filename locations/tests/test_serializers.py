from django.test import TestCase
from django.contrib.gis.geos import Point
from locations.models import Location
from locations.serializers import LocationSerializer, LocationListSerializer


class LocationSerializerTest(TestCase):
    

    def setUp(self):
        
        self.location_data = {
            'name': 'Test Location',
            'description': 'A test location',
            'address': '123 Test St',
            'point': Point(-74.0060, 40.7128, srid=4326)
        }
        self.location = Location.objects.create(**self.location_data)

    def test_location_serializer_contains_expected_fields(self):
        
        serializer = LocationSerializer(instance=self.location)
        data = serializer.data
        
        self.assertIn('id', data['properties'])
        self.assertIn('name', data['properties'])
        self.assertIn('description', data['properties'])
        self.assertIn('address', data['properties'])
        self.assertIn('latitude', data['properties'])
        self.assertIn('longitude', data['properties'])
        self.assertIn('created_at', data['properties'])
        self.assertIn('updated_at', data['properties'])

    def test_location_serializer_geojson_format(self):
        
        serializer = LocationSerializer(instance=self.location)
        data = serializer.data
        
        self.assertEqual(data['type'], 'Feature')
        self.assertIn('geometry', data)
        self.assertIn('properties', data)
        self.assertEqual(data['geometry']['type'], 'Point')
        self.assertEqual(len(data['geometry']['coordinates']), 2)

    def test_location_serializer_coordinates(self):
        
        serializer = LocationSerializer(instance=self.location)
        data = serializer.data
        
        lon, lat = data['geometry']['coordinates']
        self.assertAlmostEqual(lon, -74.0060, places=4)
        self.assertAlmostEqual(lat, 40.7128, places=4)

    def test_location_serializer_create(self):
        
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-73.9857, 40.7484]
            },
            'properties': {
                'name': 'Empire State Building',
                'description': 'Famous skyscraper',
                'address': '350 5th Ave, New York, NY'
            }
        }
        
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        location = serializer.save()
        
        self.assertEqual(location.name, 'Empire State Building')
        self.assertAlmostEqual(location.longitude, -73.9857, places=4)
        self.assertAlmostEqual(location.latitude, 40.7484, places=4)

    def test_location_list_serializer(self):
        
        serializer = LocationListSerializer(instance=self.location)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('latitude', data)
        self.assertIn('longitude', data)
        self.assertNotIn('geometry', data)  

    def test_location_serializer_validation(self):
        
        invalid_data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-73.9857, 40.7484]
            },
            'properties': {
                
                'description': 'Test'
            }
        }
        
        serializer = LocationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors['properties'])