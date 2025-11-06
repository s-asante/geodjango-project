import pytest
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient
from .factories import UserFactory, AdminUserFactory, LocationFactory, NYCLocationFactory


@pytest.fixture
def api_client():
    
    return APIClient()


@pytest.fixture
def user():
    
    return UserFactory()


@pytest.fixture
def admin_user():
    
    return AdminUserFactory()


@pytest.fixture
def authenticated_client(api_client, user):
    
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def location():
    
    return LocationFactory()


@pytest.fixture
def nyc_location():
    
    return NYCLocationFactory()


@pytest.fixture
def locations():
    
    return LocationFactory.create_batch(5)


@pytest.fixture
def nyc_locations():
    
    return NYCLocationFactory.create_batch(5)


@pytest.fixture
def sample_point():
    
    return Point(-74.0060, 40.7128, srid=4326)