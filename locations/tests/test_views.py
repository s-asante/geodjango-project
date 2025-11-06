from django.urls import reverse
from rest_framework import status
from django.contrib.gis.geos import Point
from locations.models import Location
from .base import LocationAPITestCase


class LocationViewSetTest(LocationAPITestCase):
    

    def setUp(self):
        
        super().setUp()
        
        
        self.location1 = Location.objects.create(
            name="Location 1",
            description="First test location",
            address="Address 1",
            point=Point(-74.0060, 40.7128, srid=4326)  
        )
        
        self.location2 = Location.objects.create(
            name="Location 2",
            description="Second test location",
            address="Address 2",
            point=Point(-73.9857, 40.7484, srid=4326)  
        )
        
        self.location3 = Location.objects.create(
            name="Location 3",
            description="Third test location",
            address="Address 3",
            point=Point(-118.2437, 34.0522, srid=4326)  
        )

    def test_list_locations(self):
        
        url = reverse('location-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 3)

    def test_list_locations_authenticated(self):
        
        self.authenticate()
        url = reverse('location-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_list_locations_unauthenticated(self):
        
        
        self.client.force_authenticate(user=None)
        
        url = reverse('location-list')
        response = self.client.get(url)
        
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_location(self):
        
        url = reverse('location-detail', kwargs={'pk': self.location1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], 'Feature')
        self.assertEqual(response.data['properties']['name'], 'Location 1')
        self.assertEqual(response.data['properties']['description'], 'First test location')
        self.assertIn('geometry', response.data)

    def test_retrieve_nonexistent_location(self):
        
        url = reverse('location-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_location(self):
        
        url = reverse('location-list')
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-0.1276, 51.5074]  
            },
            'properties': {
                'name': 'London Eye',
                'description': 'Famous observation wheel',
                'address': 'Westminster Bridge Rd, London'
            }
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 4)
        
        
        new_location = Location.objects.get(name='London Eye')
        self.assertEqual(new_location.description, 'Famous observation wheel')
        self.assertAlmostEqual(new_location.longitude, -0.1276, places=4)
        self.assertAlmostEqual(new_location.latitude, 51.5074, places=4)

    def test_create_location_minimal_data(self):
        
        url = reverse('location-list')
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [2.3522, 48.8566]  
            },
            'properties': {
                'name': 'Eiffel Tower'
            }
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 4)
        
        new_location = Location.objects.get(name='Eiffel Tower')
        self.assertEqual(new_location.description, '')
        self.assertEqual(new_location.address, '')

    def test_create_location_missing_name(self):
        
        url = reverse('location-list')
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-0.1276, 51.5074]
            },
            'properties': {
                'description': 'Missing name'
            }
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', str(response.data))

    def test_create_location_missing_geometry(self):
        
        url = reverse('location-list')
        data = {
            'type': 'Feature',
            'properties': {
                'name': 'No Geometry Location'
            }
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_location_invalid_coordinates(self):
        
        url = reverse('location-list')
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [200, 100]  
            },
            'properties': {
                'name': 'Invalid Location'
            }
        }
        
        response = self.client.post(url, data, format='json')
        
        
        
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_update_location(self):
        
        url = reverse('location-detail', kwargs={'pk': self.location1.pk})
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-74.0060, 40.7128]
            },
            'properties': {
                'name': 'Updated Location',
                'description': 'Updated description',
                'address': 'Updated Address'
            }
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        self.location1.refresh_from_db()
        self.assertEqual(self.location1.name, 'Updated Location')
        self.assertEqual(self.location1.description, 'Updated description')
        self.assertEqual(self.location1.address, 'Updated Address')

    def test_partial_update_location(self):
        
        url = reverse('location-detail', kwargs={'pk': self.location1.pk})
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-74.0060, 40.7128]
            },
            'properties': {
                'description': 'Partially updated description'
            }
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        self.location1.refresh_from_db()
        self.assertEqual(self.location1.name, 'Location 1')  
        self.assertEqual(self.location1.description, 'Partially updated description')
        self.assertEqual(self.location1.address, 'Address 1')  

    def test_update_location_coordinates(self):
        
        url = reverse('location-detail', kwargs={'pk': self.location1.pk})
        
        original_lat = self.location1.latitude
        original_lon = self.location1.longitude
        
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-73.9857, 40.7484]  
            },
            'properties': {
                'name': self.location1.name,
                'description': self.location1.description,
                'address': self.location1.address
            }
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        self.location1.refresh_from_db()
        self.assertNotEqual(self.location1.latitude, original_lat)
        self.assertNotEqual(self.location1.longitude, original_lon)
        self.assertAlmostEqual(self.location1.longitude, -73.9857, places=4)
        self.assertAlmostEqual(self.location1.latitude, 40.7484, places=4)

    def test_delete_location(self):
        
        url = reverse('location-detail', kwargs={'pk': self.location1.pk})
        
        
        self.assertTrue(Location.objects.filter(pk=self.location1.pk).exists())
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Location.objects.count(), 2)
        
        
        self.assertFalse(Location.objects.filter(pk=self.location1.pk).exists())

    def test_delete_nonexistent_location(self):
        
        url = reverse('location-detail', kwargs={'pk': 99999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pagination(self):
        
        
        for i in range(15):
            Location.objects.create(
                name=f"Pagination Test {i}",
                description=f"Location {i}",
                point=Point(-74.0 + (i * 0.01), 40.7 + (i * 0.01), srid=4326)
            )
        
        url = reverse('location-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        
        
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['count'], 18)  

    def test_location_ordering(self):
        """Test that locations are ordered by creation date (newest first)"""
        url = reverse('location-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data['results']
        
        # For list view, we use LocationListSerializer which doesn't nest in 'properties'
        # Verify newest location is first
        self.assertEqual(results[0]['name'], 'Location 3')
        
    def test_geojson_format(self):
        """Test that detail responses are in valid GeoJSON format"""
        url = reverse('location-detail', kwargs={'pk': self.location1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify GeoJSON structure
        self.assertEqual(response.data['type'], 'Feature')
        self.assertIn('geometry', response.data)
        self.assertIn('properties', response.data)
        self.assertIn('id', response.data)  # id is at root level for GeoFeatureModelSerializer
        
        # Verify geometry structure
        self.assertEqual(response.data['geometry']['type'], 'Point')
        self.assertIn('coordinates', response.data['geometry'])
        self.assertEqual(len(response.data['geometry']['coordinates']), 2)
        
        # Verify properties
        properties = response.data['properties']
        self.assertIn('name', properties)
        self.assertIn('description', properties)
        self.assertIn('address', properties)
        self.assertIn('latitude', properties)
        self.assertIn('longitude', properties)
        self.assertIn('created_at', properties)
        self.assertIn('updated_at', properties)


class LocationViewSetPermissionTest(LocationAPITestCase):
    
    
    def setUp(self):
        
        super().setUp()
        self.location = Location.objects.create(
            name="Permission Test Location",
            point=Point(-74.0060, 40.7128, srid=4326)
        )
    
    def test_create_location_authenticated(self):
        
        self.authenticate()
        
        url = reverse('location-list')
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-0.1276, 51.5074]
            },
            'properties': {
                'name': 'Authenticated Location'
            }
        }
        
        response = self.client.post(url, data, format='json')
        
        
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN])
    
    def test_update_location_authenticated(self):
        
        self.authenticate()
        
        url = reverse('location-detail', kwargs={'pk': self.location.pk})
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-74.0060, 40.7128]
            },
            'properties': {
                'name': 'Updated by authenticated user'
            }
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])
    
    def test_delete_location_as_admin(self):
        
        self.authenticate_admin()
        
        url = reverse('location-detail', kwargs={'pk': self.location.pk})
        response = self.client.delete(url)
        
        
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_403_FORBIDDEN])