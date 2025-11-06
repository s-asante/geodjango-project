from django.test import TestCase, TransactionTestCase
from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from locations.models import Location


class BaseTestCase(TestCase):
    
    
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
    
    def setUp(self):
        
        
        pass
    
    def tearDown(self):
        
        
        pass


class LocationTestMixin:
    
    
    def create_location(self, name="Test Location", lon=-74.0060, lat=40.7128, **kwargs):
        
        defaults = {
            'name': name,
            'description': kwargs.get('description', 'Test description'),
            'address': kwargs.get('address', 'Test address'),
            'point': Point(lon, lat, srid=4326)
        }
        defaults.update(kwargs)
        return Location.objects.create(**defaults)
    
    def create_multiple_locations(self, count=3):
        
        locations = []
        coordinates = [
            (-74.0060, 40.7128),  
            (-73.9857, 40.7484),  
            (-73.9654, 40.7829),  
        ]
        
        for i in range(count):
            lon, lat = coordinates[i % len(coordinates)]
            location = self.create_location(
                name=f"Location {i+1}",
                lon=lon + (i * 0.01),  
                lat=lat + (i * 0.01)
            )
            locations.append(location)
        
        return locations
    
    def assertLocationEqual(self, location1, location2, check_timestamps=False):
        
        self.assertEqual(location1.name, location2.name)
        self.assertEqual(location1.description, location2.description)
        self.assertEqual(location1.address, location2.address)
        self.assertAlmostEqual(location1.latitude, location2.latitude, places=4)
        self.assertAlmostEqual(location1.longitude, location2.longitude, places=4)
        
        if check_timestamps:
            self.assertEqual(location1.created_at, location2.created_at)
            self.assertEqual(location1.updated_at, location2.updated_at)


class LocationAPITestCase(APITestCase, LocationTestMixin):
    
    
    @classmethod
    def setUpTestData(cls):
        
        cls.user = User.objects.create_user(
            username='apiuser',
            password='apipass123'
        )
        cls.admin_user = User.objects.create_superuser(
            username='apiadmin',
            password='adminpass123'
        )
    
    def setUp(self):
        
        self.client = APIClient()
    
    def authenticate(self, user=None):
        
        if user is None:
            user = self.user
        self.client.force_authenticate(user=user)
    
    def authenticate_admin(self):
        
        self.authenticate(user=self.admin_user)


class LocationTransactionTestCase(TransactionTestCase, LocationTestMixin):
   
    def setUp(self):
        
        super().setUp()
        self.user = User.objects.create_user(
            username='transuser',
            password='transpass123'
        )