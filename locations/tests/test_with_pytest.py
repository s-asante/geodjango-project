import pytest
from django.urls import reverse
from rest_framework import status
from locations.models import Location


@pytest.mark.django_db
class TestLocationAPI:
    
    
    def test_list_locations(self, api_client, locations):
        
        url = reverse('location-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
    
    def test_create_location_authenticated(self, authenticated_client):
        
        url = reverse('location-list')
        data = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [-74.0060, 40.7128]
            },
            'properties': {
                'name': 'Test Location',
                'description': 'Test description',
                'address': 'Test address'
            }
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Location.objects.filter(name='Test Location').exists()
    
    def test_retrieve_location(self, api_client, location):
        
        url = reverse('location-detail', kwargs={'pk': location.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['properties']['name'] == location.name
    
    @pytest.mark.parametrize('distance', [1000, 5000, 10000])
    def test_nearby_locations_different_distances(
        self, api_client, nyc_locations, distance
    ):
        
        url = reverse('location-nearby')
        response = api_client.get(url, {
            'lat': 40.7128,
            'lon': -74.0060,
            'distance': distance
        })
        
        assert response.status_code == status.HTTP_200_OK
        