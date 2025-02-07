# Variables
DOCKER_COMPOSE = docker-compose
PYTHON = python3
PIP = pip
ALEMBIC = alembic
ENV_FILE = .env

# Default target
.DEFAULT_GOAL := help

# Help target
help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Docker commands
up:  ## Start the Docker containers
	$(DOCKER_COMPOSE) up --build

down:  ## Stop and remove the Docker containers
	$(DOCKER_COMPOSE) down

restart: down up ## Restart the Docker containers

logs:  ## Show logs for the Docker containers
	$(DOCKER_COMPOSE) logs -f

# Database commands
migrate:  ## Run database migrations
	$(ALEMBIC) upgrade head

makemigrations:  ## Create a new Alembic migration
	$(ALEMBIC) revision --autogenerate -m "New migration"

resetdb:  ## Reset the database (drops and recreates tables)
	$(ALEMBIC) downgrade base
	$(ALEMBIC) upgrade head

# Python environment commands
install:  ## Install Python dependencies
	$(PIP) install -r requirements.txt

freeze:  ## Freeze Python dependencies into requirements.txt
	$(PIP) freeze > requirements.txt

lint:  ## Run linting (e.g., flake8 or black)
	black . --check

format:  ## Format code using black
	black .

test:  ## Run tests using pytest
	pytest

# Clean up commands
clean:  ## Remove Python cache files
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

clean-docker:  ## Remove unused Docker resources
	docker system prune -f
	docker volume prune -f

# Firebase commands
firebase-init:  ## Initialize Firebase Admin SDK
	@echo "Make sure you have the Firebase service account JSON file in the project directory."
	@echo "Firebase Admin SDK initialized."

# Environment setup
env:  ## Create a .env file if it doesn't exist
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "Creating .env file..."; \
		touch $(ENV_FILE); \
		echo "DATABASE_URL=postgresql://your_user:your_password@db:5432/your_database" >> $(ENV_FILE); \
		echo "Environment file created."; \
	else \
		echo ".env file already exists."; \
	fi