# GeoDjango REST API Project

A Django REST Framework project with PostGIS support for managing geographic locations.

## Prerequisites

- Python 3.10+
- Docker and Docker Compose
- UV package manager
- GDAL libraries

## Setup

1. Install UV:
```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install system dependencies:
```bash
   sudo apt-get install gdal-bin libgdal-dev
```

3. Start PostgreSQL with PostGIS:
```bash
   make docker-up
```

4. Install Python dependencies:
```bash
   make install
```

5. Run migrations:
```bash
   make migrate
```

6. Create superuser:
```bash
   uv run python manage.py createsuperuser
```

7. Load sample data:
```bash
   make sample-data
```

8. Run the server:
```bash
   make run
```

## API Endpoints

- `GET /api/locations/` - List all locations
- `POST /api/locations/` - Create a new location
- `GET /api/locations/{id}/` - Get location details
- `PUT /api/locations/{id}/` - Update location
- `DELETE /api/locations/{id}/` - Delete location
- `GET /api/locations/nearby/?lat=40.7128&lon=-74.0060&distance=5000` - Find nearby locations
- `GET /api/locations/within_bounds/?min_lat=40.7&max_lat=40.8&min_lon=-74.1&max_lon=-74.0` - Find locations within bounds

## Testing
```bash
# Test nearby locations
curl "http://localhost:8000/api/locations/nearby/?lat=40.7484&lon=-73.9857&distance=2000"

# Create a location
curl -X POST http://localhost:8000/api/locations/ \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-73.935242, 40.730610]},
    "properties": {"name": "Test Location", "description": "A test location", "address": "Test Address"}
  }'
```