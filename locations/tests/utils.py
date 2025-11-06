from django.contrib.gis.geos import Point
import random


def generate_random_point(min_lon=-180, max_lon=180, min_lat=-90, max_lat=90):
    
    lon = random.uniform(min_lon, max_lon)
    lat = random.uniform(min_lat, max_lat)
    return Point(lon, lat, srid=4326)


def generate_nyc_point():
    
    return generate_random_point(
        min_lon=-74.1,
        max_lon=-73.9,
        min_lat=40.6,
        max_lat=40.9
    )


def assert_geojson_valid(test_case, geojson_data):
    
    test_case.assertIn('type', geojson_data)
    test_case.assertEqual(geojson_data['type'], 'Feature')
    test_case.assertIn('geometry', geojson_data)
    test_case.assertIn('properties', geojson_data)
    test_case.assertEqual(geojson_data['geometry']['type'], 'Point')


def calculate_distance_km(point1, point2):
    
    from django.contrib.gis.measure import D
    from django.contrib.gis.db.models.functions import Distance
    
    
    import math
    
    lon1, lat1 = point1.x, point1.y
    lon2, lat2 = point2.x, point2.y
    
    R = 6371  
    
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    
    a = (math.sin(dLat/2) * math.sin(dLat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon/2) * math.sin(dLon/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c