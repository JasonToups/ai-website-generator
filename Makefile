.PHONY: help install setup dev backend frontend test lint format build start clean reset logs

# Default target
help:
	@echo "AI Website Generator - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup     - Complete project setup (install deps, create .env if needed)"
	@echo "  make install   - Install all dependencies (backend and frontend)"
	@echo ""
	@echo "Development:"
	@echo "  make dev       - Start both backend and frontend in development mode"
	@echo "  make backend   - Start only the FastAPI backend server"
	@echo "  make frontend  - Start only the React frontend server"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test      - Run all tests"
	@echo "  make lint      - Run linting for both Python and TypeScript"
	@echo "  make format    - Format code (black for Python, prettier for TypeScript)"
	@echo ""
	@echo "Production:"
	@echo "  make build     - Build the frontend for production"
	@echo "  make start     - Start production server"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean     - Clean up build artifacts and caches"
	@echo "  make reset     - Reset project state (clean + fresh install)"
	@echo "  make logs      - Show recent application logs"
	@echo "  make env       - Create .env file from template"
	@echo ""

# Setup & Installation
setup: install env
	@echo "✅ Project setup complete!"
	@echo "📝 Don't forget to add your ANTHROPIC_API_KEY to the .env file"
	@echo "🚀 Run 'make dev' to start development servers"

install:
	@echo "📦 Installing backend dependencies..."
	poetry install
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ All dependencies installed!"

env:
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file from template..."; \
		cp .env.example .env; \
		echo "✅ .env file created! Please add your ANTHROPIC_API_KEY"; \
	else \
		echo "✅ .env file already exists"; \
	fi

# Development
dev:
	@echo "🚀 Starting development servers..."
	@echo "Backend will be available at: http://localhost:8000"
	@echo "Frontend will be available at: http://localhost:5173"
	@echo "API docs will be available at: http://localhost:8000/docs"
	@echo ""
	@trap 'kill %1; kill %2' INT; \
	make backend & \
	make frontend & \
	wait

backend:
	@echo "🐍 Starting FastAPI backend server..."
	poetry run python -m backend.main

frontend:
	@echo "⚛️  Starting React frontend server..."
	cd frontend && npm run dev

# Testing & Quality
test:
	@echo "🧪 Running backend tests..."
	poetry run pytest
	@echo "🧪 Running frontend tests..."
	cd frontend && npm run test

lint:
	@echo "🔍 Linting Python code..."
	poetry run flake8 backend/
	poetry run mypy backend/
	@echo "🔍 Linting TypeScript code..."
	cd frontend && npm run lint

format:
	@echo "🎨 Formatting Python code..."
	poetry run black backend/
	poetry run isort backend/
	@echo "🎨 Formatting TypeScript code..."
	cd frontend && npm run format

# Production
build:
	@echo "🏗️  Building frontend for production..."
	cd frontend && npm run build
	@echo "✅ Frontend build complete!"

start:
	@echo "🚀 Starting production server..."
	poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Utilities
clean:
	@echo "🧹 Cleaning up..."
	rm -rf backend/__pycache__/
	rm -rf backend/*/__pycache__/
	rm -rf backend/*/*/__pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf frontend/node_modules/.cache/
	rm -rf frontend/dist/
	@echo "✅ Cleanup complete!"

reset: clean
	@echo "🔄 Resetting project..."
	rm -rf frontend/node_modules/
	poetry env remove --all 2>/dev/null || true
	make install
	@echo "✅ Project reset complete!"

logs:
	@echo "📋 Recent application logs:"
	@if [ -f data/app.log ]; then \
		tail -50 data/app.log; \
	else \
		echo "No log file found. Start the application to generate logs."; \
	fi

# Health check
health:
	@echo "🏥 Checking application health..."
	@curl -s http://localhost:8000/health || echo "❌ Backend not responding"
	@curl -s http://localhost:5173 > /dev/null && echo "✅ Frontend is running" || echo "❌ Frontend not responding"

# Database/Data management
data-clean:
	@echo "🗑️  Cleaning project data..."
	rm -rf data/projects.json
	rm -rf generated/projects/*
	@echo "✅ Project data cleaned!"

# Quick commands for common workflows
quick-start: setup dev

quick-test: format lint test

deploy-prep: format lint test build
	@echo "🚀 Ready for deployment!"

# Development helpers
install-dev-tools:
	@echo "🛠️  Installing additional development tools..."
	poetry add --group dev pre-commit
	cd frontend && npm install --save-dev prettier eslint-config-prettier
	@echo "✅ Development tools installed!"

# Show project status
status:
	@echo "📊 Project Status:"
	@echo "Backend dependencies: $(shell poetry show | wc -l) packages"
	@echo "Frontend dependencies: $(shell cd frontend && npm list --depth=0 2>/dev/null | grep -c '├\|└' || echo 'unknown')"
	@echo "Python version: $(shell poetry run python --version)"
	@echo "Node version: $(shell node --version)"
	@echo "Generated projects: $(shell find generated/projects -name "*.txt" 2>/dev/null | wc -l)"
