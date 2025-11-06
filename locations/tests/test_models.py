from django.test import TestCase
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from locations.models import Location
from .base import BaseTestCase, LocationTestMixin


class LocationModelTest(BaseTestCase, LocationTestMixin):
    

    def setUp(self):
        
        self.location = self.create_location(
            name="Test Location",
            description="A test location",
            address="123 Test St, Test City",
            lon=-74.0060,
            lat=40.7128
        )

    def test_location_creation(self):
        
        self.assertEqual(self.location.name, "Test Location")
        self.assertEqual(self.location.description, "A test location")
        self.assertEqual(self.location.address, "123 Test St, Test City")
        self.assertIsNotNone(self.location.point)
        self.assertIsNotNone(self.location.id)

    def test_location_creation_minimal(self):
        
        minimal_location = Location.objects.create(
            name="Minimal Location",
            point=Point(-73.9857, 40.7484, srid=4326)
        )
        
        self.assertEqual(minimal_location.name, "Minimal Location")
        self.assertEqual(minimal_location.description, "")
        self.assertEqual(minimal_location.address, "")
        self.assertIsNotNone(minimal_location.point)

    def test_multiple_locations_creation(self):
        
        locations = self.create_multiple_locations(5)
        
        self.assertEqual(len(locations), 5)
        self.assertEqual(Location.objects.count(), 6)  
        
        
        location_names = [loc.name for loc in locations]
        self.assertEqual(len(location_names), len(set(location_names)))

    def test_location_str_method(self):
        
        self.assertEqual(str(self.location), "Test Location")
        
        
        location2 = self.create_location(name="Another Location")
        self.assertEqual(str(location2), "Another Location")

    def test_location_coordinates(self):
        
        self.assertAlmostEqual(self.location.point.x, -74.0060, places=4)
        self.assertAlmostEqual(self.location.point.y, 40.7128, places=4)
        
        
        self.assertTrue(self.location.point.valid)

    def test_latitude_property(self):
        
        self.assertAlmostEqual(self.location.latitude, 40.7128, places=4)
        
        
        location2 = self.create_location(lat=51.5074)
        self.assertAlmostEqual(location2.latitude, 51.5074, places=4)

    def test_longitude_property(self):
        
        self.assertAlmostEqual(self.location.longitude, -74.0060, places=4)
        
        
        location2 = self.create_location(lon=-0.1276)
        self.assertAlmostEqual(location2.longitude, -0.1276, places=4)

    def test_location_srid(self):
        
        self.assertEqual(self.location.point.srid, 4326)
        
        
        location2 = Location.objects.create(
            name="SRID Test",
            point=Point(-73.9857, 40.7484, srid=4326)
        )
        self.assertEqual(location2.point.srid, 4326)

    def test_location_timestamps(self):
        
        self.assertIsNotNone(self.location.created_at)
        self.assertIsNotNone(self.location.updated_at)
        
        
        self.assertAlmostEqual(
            self.location.created_at.timestamp(),
            self.location.updated_at.timestamp(),
            places=0
        )

    def test_location_updated_at_changes(self):
        
        import time
        
        original_updated_at = self.location.updated_at
        
        
        time.sleep(0.1)
        
        
        self.location.description = "Updated description"
        self.location.save()
        
        
        self.location.refresh_from_db()
        
        
        self.assertGreater(self.location.updated_at, original_updated_at)

    def test_location_ordering(self):
        
        location2 = Location.objects.create(
            name="Second Location",
            description="Another location",
            point=Point(-73.9857, 40.7484, srid=4326)
        )
        
        location3 = Location.objects.create(
            name="Third Location",
            description="Yet another location",
            point=Point(-73.9654, 40.7829, srid=4326)
        )
        
        locations = Location.objects.all()
        
        
        self.assertEqual(locations[0], location3)
        self.assertEqual(locations[1], location2)
        self.assertEqual(locations[2], self.location)

    def test_blank_fields(self):
        
        location = Location.objects.create(
            name="Minimal Location",
            point=Point(-73.9857, 40.7484, srid=4326)
        )
        
        self.assertEqual(location.description, "")
        self.assertEqual(location.address, "")
        
        
        self.assertIsNotNone(location.description)
        self.assertIsNotNone(location.address)

    def test_location_name_max_length(self):
        
        long_name = "A" * 200  
        location = Location.objects.create(
            name=long_name,
            point=Point(-73.9857, 40.7484, srid=4326)
        )
        
        self.assertEqual(len(location.name), 200)
        self.assertEqual(location.name, long_name)

    def test_location_address_max_length(self):
        
        long_address = "A" * 300  
        location = Location.objects.create(
            name="Address Test",
            address=long_address,
            point=Point(-73.9857, 40.7484, srid=4326)
        )
        
        self.assertEqual(len(location.address), 300)
        self.assertEqual(location.address, long_address)

    def test_location_update(self):
        
        original_name = self.location.name
        original_point = self.location.point
        
        
        self.location.name = "Updated Location"
        self.location.description = "Updated description"
        self.location.point = Point(-73.9857, 40.7484, srid=4326)
        self.location.save()
        
        
        self.location.refresh_from_db()
        
        self.assertEqual(self.location.name, "Updated Location")
        self.assertEqual(self.location.description, "Updated description")
        self.assertNotEqual(self.location.point, original_point)

    def test_location_delete(self):
        
        location_id = self.location.id
        self.location.delete()
        
        
        with self.assertRaises(Location.DoesNotExist):
            Location.objects.get(id=location_id)

    def test_location_queryset_filter_by_name(self):
        
        self.create_location(name="Unique Name 1")
        self.create_location(name="Unique Name 2")
        
        results = Location.objects.filter(name__icontains="Unique")
        self.assertEqual(results.count(), 2)
        
        results = Location.objects.filter(name="Unique Name 1")
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().name, "Unique Name 1")

    def test_location_queryset_filter_by_description(self):
        
        self.create_location(
            name="Location 1",
            description="Contains keyword restaurant"
        )
        self.create_location(
            name="Location 2",
            description="Contains keyword museum"
        )
        
        results = Location.objects.filter(description__icontains="restaurant")
        self.assertEqual(results.count(), 1)

    def test_location_point_not_null(self):
        
        with self.assertRaises(IntegrityError):
            Location.objects.create(
                name="No Point Location",
                point=None
            )

    def test_location_name_not_blank(self):
        
        with self.assertRaises(ValidationError):
            location = Location(
                name="",
                point=Point(-73.9857, 40.7484, srid=4326)
            )
            location.full_clean()

    def test_location_different_coordinates(self):
        
        
        ny_location = Location.objects.create(
            name="New York",
            point=Point(-74.0060, 40.7128, srid=4326)
        )
        
        
        london_location = Location.objects.create(
            name="London",
            point=Point(-0.1276, 51.5074, srid=4326)
        )
        
        
        tokyo_location = Location.objects.create(
            name="Tokyo",
            point=Point(139.6917, 35.6895, srid=4326)
        )
        
        
        self.assertEqual(ny_location.point.srid, 4326)
        self.assertEqual(london_location.point.srid, 4326)
        self.assertEqual(tokyo_location.point.srid, 4326)
        
        
        self.assertNotEqual(ny_location.point, london_location.point)
        self.assertNotEqual(ny_location.point, tokyo_location.point)
        self.assertNotEqual(london_location.point, tokyo_location.point)

    def test_location_meta_verbose_names(self):
        
        self.assertEqual(Location._meta.verbose_name, 'Location')
        self.assertEqual(Location._meta.verbose_name_plural, 'Locations')

    def test_location_count(self):
        
        initial_count = Location.objects.count()
        self.assertEqual(initial_count, 1)  
        
        
        self.create_multiple_locations(10)
        
        final_count = Location.objects.count()
        self.assertEqual(final_count, 11)  

    def test_location_exists(self):
        
        self.assertTrue(
            Location.objects.filter(name="Test Location").exists()
        )
        
        self.assertFalse(
            Location.objects.filter(name="Nonexistent Location").exists()
        )

    def test_location_get_or_create(self):
        
        location, created = Location.objects.get_or_create(
            name="Test Location",
            defaults={
                'description': 'Default description',
                'point': Point(-74.0060, 40.7128, srid=4326)
            }
        )
        
        self.assertFalse(created)  
        self.assertEqual(location.id, self.location.id)
        
        
        new_location, created = Location.objects.get_or_create(
            name="New Unique Location",
            defaults={
                'description': 'New description',
                'point': Point(-73.9857, 40.7484, srid=4326)
            }
        )
        
        self.assertTrue(created)
        self.assertIsNotNone(new_location.id)

    def test_location_point_geometry_type(self):
        
        self.assertEqual(self.location.point.geom_type, 'Point')
        
        
        self.assertNotEqual(self.location.point.geom_type, 'LineString')
        self.assertNotEqual(self.location.point.geom_type, 'Polygon')

    def test_location_coordinate_precision(self):
        
        precise_location = Location.objects.create(
            name="Precise Location",
            point=Point(-74.006012345, 40.712845678, srid=4326)
        )
        
        
        self.assertAlmostEqual(
            precise_location.longitude,
            -74.006012345,
            places=6
        )
        self.assertAlmostEqual(
            precise_location.latitude,
            40.712845678,
            places=6
        )


class LocationModelEdgeCasesTest(TestCase):
    
    
    def test_location_at_equator(self):
        
        location = Location.objects.create(
            name="Equator Location",
            point=Point(0, 0, srid=4326)
        )
        
        self.assertEqual(location.latitude, 0)
        self.assertEqual(location.longitude, 0)

    def test_location_at_poles(self):
        
        north_pole = Location.objects.create(
            name="North Pole",
            point=Point(0, 90, srid=4326)
        )
        
        south_pole = Location.objects.create(
            name="South Pole",
            point=Point(0, -90, srid=4326)
        )
        
        self.assertEqual(north_pole.latitude, 90)
        self.assertEqual(south_pole.latitude, -90)

    def test_location_at_date_line(self):
        
        east_location = Location.objects.create(
            name="East of Date Line",
            point=Point(180, 0, srid=4326)
        )
        
        west_location = Location.objects.create(
            name="West of Date Line",
            point=Point(-180, 0, srid=4326)
        )
        
        self.assertEqual(east_location.longitude, 180)
        self.assertEqual(west_location.longitude, -180)

    def test_location_special_characters_in_name(self):
        
        special_names = [
            "Location with émojis 🌍",
            "Café René",
            "北京",  
            "Москва",  
            "São Paulo"
        ]
        
        for name in special_names:
            location = Location.objects.create(
                name=name,
                point=Point(0, 0, srid=4326)
            )
            self.assertEqual(location.name, name)

    def test_location_very_long_description(self):
        
        long_description = "A" * 10000  
        location = Location.objects.create(
            name="Long Description",
            description=long_description,
            point=Point(0, 0, srid=4326)
        )
        
        self.assertEqual(len(location.description), 10000)
        self.assertEqual(location.description, long_description)