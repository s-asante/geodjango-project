.PHONY: help install migrate run shell test clean docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make migrate      - Run migrations"
	@echo "  make run          - Run development server"
	@echo "  make shell        - Open Django shell"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean Python cache files"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make sample-data  - Load sample locations"

install:
	uv sync

migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

run:
	uv run python manage.py runserver

shell:
	uv run python manage.py shell

test:
	uv run python manage.py test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

sample-data:
	uv run python manage.py load_sample_locations


.PHONY: test test-coverage test-verbose test-fast

test:
	uv run python manage.py test

test-verbose:
	uv run python manage.py test --verbosity=2

test-fast:
	uv run python manage.py test --parallel --keepdb

test-coverage:
	uv run coverage run --source='.' manage.py test
	uv run coverage report
	uv run coverage html

.PHONY: test test-coverage test-verbose test-fast test-models test-views test-spatial test-pytest

test:
	uv run python manage.py test

test-verbose:
	uv run python manage.py test --verbosity=2

test-fast:
	uv run python manage.py test --parallel --keepdb

test-models:
	uv run python manage.py test locations.tests.test_models

test-views:
	uv run python manage.py test locations.tests.test_views

test-spatial:
	uv run python manage.py test locations.tests.test_spatial_queries

test-coverage:
	uv run coverage run --source='.' manage.py test
	uv run coverage report
	uv run coverage html

test-pytest:
	uv run pytest -v

test-pytest-coverage:
	uv run pytest --cov=locations --cov-report=html --cov-report=term

test-with-settings:
	DJANGO_SETTINGS_MODULE=geoproject.test_settings uv run python manage.py test