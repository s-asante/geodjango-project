from django.test import TestCase
from rest_framework.test import APITestCase
from .factories import UserFactory, AdminUserFactory, LocationFactory, NYCLocationFactory
from locations.models import Location


class LocationFactoryTest(TestCase):
    
    
    def test_create_location_with_factory(self):
        
        location = LocationFactory()
        
        self.assertIsNotNone(location.id)
        self.assertIsNotNone(location.name)
        self.assertIsNotNone(location.point)
    
    def test_create_multiple_locations(self):
        
        locations = LocationFactory.create_batch(5)
        
        self.assertEqual(len(locations), 5)
        self.assertEqual(Location.objects.count(), 5)
    
    def test_create_nyc_locations(self):
        
        locations = NYCLocationFactory.create_batch(10)
        
        for location in locations:
            
            self.assertGreaterEqual(location.longitude, -74.1)
            self.assertLessEqual(location.longitude, -73.9)
            self.assertGreaterEqual(location.latitude, 40.6)
            self.assertLessEqual(location.latitude, 40.9)
    
    def test_create_location_with_custom_data(self):
        
        location = LocationFactory(
            name="Custom Location",
            description="Custom description"
        )
        
        self.assertEqual(location.name, "Custom Location")
        self.assertEqual(location.description, "Custom description")


class UserFactoryTest(TestCase):
    
    
    def test_create_user_with_factory(self):
        
        user = UserFactory()
        
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.username)
        self.assertTrue(user.check_password('defaultpass123'))
    
    def test_create_admin_user(self):
        
        admin = AdminUserFactory()
        
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
    
    def test_create_user_with_custom_password(self):
        
        user = UserFactory(password='custompass123')
        
        self.assertTrue(user.check_password('custompass123'))