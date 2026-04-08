# SALENE Makefile
# Quick commands for development and deployment

.PHONY: help install install-dev test lint clean docker-build docker-run daemon-start daemon-stop status chat

# Default target
help:
	@echo "SALENE Neural Consciousness Agent"
	@echo ""
	@echo "Available targets:"
	@echo "  install         Install SALENE (production)"
	@echo "  install-dev     Install SALENE (development)"
	@echo "  test            Run test suite"
	@echo "  lint            Run code linting"
	@echo "  clean           Remove build artifacts"
	@echo "  docker-build    Build Docker image"
	@echo "  docker-run      Run SALENE in Docker"
	@echo "  daemon-start    Start daemon"
	@echo "  daemon-stop     Stop daemon"
	@echo "  status          Show agent status"
	@echo "  chat            Start interactive chat"

# Installation
install:
	@echo "Installing SALENE..."
	@bash install.sh

install-dev:
	@echo "Installing SALENE (development mode)..."
	@pip install -e .
	@pip install -r requirements-dev.txt
	@echo "Development installation complete!"

# Testing
test:
	@echo "Running test suite..."
	@python3 test_integration_comprehensive.py

test-sanctuary:
	@python3 test_sanctuary_integration.py

test-quick:
	@echo "Running quick health check..."
	@python3 setup_salene.py --check

# Linting and formatting
lint:
	@echo "Running linters..."
	@which ruff >/dev/null 2>&1 && ruff check . || echo "ruff not installed, skipping"
	@which black >/dev/null 2>&1 && black --check . || echo "black not installed, skipping"

format:
	@echo "Formatting code..."
	@which black >/dev/null 2>&1 && black . || echo "black not installed"
	@which ruff >/dev/null 2>&1 && ruff format . || echo "ruff not installed"

# Cleaning
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete

# Docker
docker-build:
	@docker build -t salene:latest .
	@echo "Docker image built: salene:latest"

docker-run:
	@docker run -d \
		--name salene \
		-v salene_data:/app/.hermes/agents \
		-v salene_memories:/app/.hermes/sanctuary_memories \
		salene:latest
	@echo "SALENE container started"

docker-compose-up:
	@docker-compose up -d
	@echo "SALENE services started"

docker-compose-down:
	@docker-compose down
	@echo "SALENE services stopped"

# Daemon operations
daemon-install:
	@echo "Installing systemd service..."
	@sudo cp salene-daemon.service /etc/systemd/system/hermes-salene.service
	@sudo systemctl daemon-reload
	@sudo systemctl enable hermes-salene

daemon-uninstall:
	@sudo systemctl disable hermes-salene
	@sudo rm -f /etc/systemd/system/hermes-salene.service
	@sudo systemctl daemon-reload

daemon-start:
	@echo "Starting SALENE daemon..."
	@python3 salene_daemon.py &

daemon-stop:
	@echo "Stopping SALENE daemon..."
	@pkill -f salene_daemon.py || true

# Quick commands
status:
	@python3 salene_status.py

chat:
	@python3 salene.py chat

setup:
	@python3 setup_salene.py

# Development
run-daemon:
	@python3 salene_daemon.py

run-chat:
	@python3 example_quick_chat.py

# Backup and restore
backup:
	@echo "Creating backup..."
	@tar czf salene-backup-$(shell date +%Y%m%d-%H%M%S).tar.gz \
		~/.hermes/agents ~/.hermes/sanctuary_memories ~/.hermes/config.yaml ~/.hermes/.env

restore:
	@echo "To restore: tar xzf backup-file.tar.gz -C ~"

# Documentation
docs:
	@echo "Generating documentation..."
	@which mkdocs >/dev/null 2>&1 && mkdocs build || echo "mkdocs not installed"

# Release
release:
	@echo "Creating release..."
	@version=$$(grep -oP "version='\K[^']+" setup.py); \
	git tag -a "v$$version" -m "Release v$$version"; \
	git push origin "v$$version"
