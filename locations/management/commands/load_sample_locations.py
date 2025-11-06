from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from locations.models import Location

class Command(BaseCommand):
    help = 'Load sample location data'

    def handle(self, *args, **kwargs):
        sample_locations = [
            {
                'name': 'Statue of Liberty',
                'description': 'Iconic statue in New York Harbor',
                'address': 'Liberty Island, New York, NY 10004',
                'lat': 40.6892,
                'lon': -74.0445
            },
            {
                'name': 'Empire State Building',
                'description': '102-story Art Deco skyscraper',
                'address': '20 W 34th St, New York, NY 10001',
                'lat': 40.7484,
                'lon': -73.9857
            },
            {
                'name': 'Central Park',
                'description': 'Urban park in Manhattan',
                'address': 'New York, NY',
                'lat': 40.7829,
                'lon': -73.9654
            },
            {
                'name': 'Brooklyn Bridge',
                'description': 'Historic hybrid cable-stayed/suspension bridge',
                'address': 'New York, NY 10038',
                'lat': 40.7061,
                'lon': -73.9969
            },
        ]

        for loc_data in sample_locations:
            location, created = Location.objects.get_or_create(
                name=loc_data['name'],
                defaults={
                    'description': loc_data['description'],
                    'address': loc_data['address'],
                    'point': Point(loc_data['lon'], loc_data['lat'], srid=4326)
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created location: {location.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Location already exists: {location.name}')
                )