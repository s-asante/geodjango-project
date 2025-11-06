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