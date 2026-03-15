# Makefile for Kenali Diri API (Python/FastAPI)

# Default Environment: dev (can be overridden with ENV=prod)
ENV ?= dev
COMPOSE_FILE = docker-compose.$(ENV).yml

# Local Commands
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

migrate:
	alembic upgrade head

seeder:
	python scripts/seed_all.py

test:
	pytest tests/

# Docker Commands (matching Golang backend pattern)
up:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down

reset:
	docker compose -f $(COMPOSE_FILE) down -v

build-docker:
	docker compose -f $(COMPOSE_FILE) up -d --build

# Docker Execute Commands
docker-migrate:
	docker compose -f $(COMPOSE_FILE) exec -T api alembic upgrade head

docker-seeder:
	docker compose -f $(COMPOSE_FILE) exec -T api python scripts/seed_all.py

docker-both:
	docker compose -f $(COMPOSE_FILE) exec -T api alembic upgrade head
	docker compose -f $(COMPOSE_FILE) exec -T api python scripts/seed_all.py

help:
	@echo "Usage: make [target] [ENV=dev|prod]"
	@echo "Targets:"
	@echo "  run             Run FastAPI app locally"
	@echo "  migrate         Run alembic migrations locally"
	@echo "  seeder          Run seeders locally"
	@echo "  test            Run pytest"
	@echo "  up              Start Docker containers (default: dev)"
	@echo "  down            Stop Docker containers"
	@echo "  reset           Stop and remove volumes"
	@echo "  build-docker    Build and start Docker containers"
	@echo "  docker-migrate  Run migrations inside Docker container"
	@echo "  docker-seeder   Run seeders inside Docker container"
	@echo "  docker-both     Run migrate + seeder inside Docker container"
