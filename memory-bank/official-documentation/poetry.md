# Poetry Documentation - Python Dependency Management

## Overview

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

## Basic Usage

### Project Setup

#### Creating a New Project

```bash
poetry new poetry-demo
```

This creates a directory structure:

```
poetry-demo
├── pyproject.toml
├── README.md
├── src
│   └── poetry_demo
│       └── __init__.py
└── tests
    └── __init__.py
```

#### Initializing an Existing Project

```bash
cd pre-existing-project
poetry init
```

### Project Configuration

#### pyproject.toml Structure

```toml
[project]
name = "poetry-demo"
version = "0.1.0"
description = ""
authors = [
    {name = "Sébastien Eustace", email = "sebastien@eustace.io"}
]
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

### Operating Modes

#### Package Mode (Default)

- Used when you want to package your project into an sdist or wheel
- Metadata like `name` and `version` are required
- Project is installed in editable mode with `poetry install`

#### Non-Package Mode

```toml
[tool.poetry]
package-mode = false
```

- Used for dependency management only
- Metadata like `name` and `version` are optional
- Project itself is not installed, only dependencies

### Python Version Management

#### Setting Python Version

```toml
[project]
requires-python = ">=3.9"
```

**Important**: Poetry requires you to have a compatible Python interpreter available on your system. It will not install Python for you.

### Dependency Management

#### Adding Dependencies

```bash
# Add a dependency
poetry add pendulum

# Add with version constraints
poetry add "pendulum>=2.1,<3.0"

# Add development dependencies
poetry add pytest --group dev
```

#### Manual Dependency Specification

```toml
[project]
dependencies = [
    "pendulum>=2.1,<3.0"
]

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.0.0"
```

### Virtual Environment Management

#### Using Poetry's Virtual Environment

```bash
# Install dependencies
poetry install

# Run commands in virtual environment
poetry run python your_script.py
poetry run pytest

# Activate virtual environment
poetry shell
```

#### Virtual Environment Location

- Default: `{cache-dir}/virtualenvs`
- Can be configured to create in project directory:

```bash
poetry config virtualenvs.in-project true
```

### Installing Dependencies

#### First Installation (without poetry.lock)

- Poetry resolves all dependencies
- Downloads latest compatible versions
- Creates `poetry.lock` file with exact versions
- Commit `poetry.lock` to version control

#### Subsequent Installations (with poetry.lock)

- Uses exact versions from `poetry.lock`
- Ensures consistent environments across team
- Faster installation process

### Version Constraints

#### Constraint Types

- **Caret constraints**: `^1.2.3` (>=1.2.3, <2.0.0)
- **Tilde constraints**: `~1.2.3` (>=1.2.3, <1.3.0)
- **Exact constraints**: `1.2.3`
- **Range constraints**: `>=1.2.3,<2.0.0`

### Updating Dependencies

```bash
# Update all dependencies
poetry update

# Update specific dependency
poetry update requests

# Update within constraints
poetry update --dry-run  # Preview changes
```

## Configuration for Our AI Website Builder

### Recommended pyproject.toml

```toml
[tool.poetry]
name = "ai-website-generator"
version = "0.1.0"
description = "AI-powered website builder using CrewAI"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "backend"}]

[tool.poetry.dependencies]
python = "^3.9"
crewai = "^0.1.0"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
anthropic = "^0.7.0"
pydantic = "^2.5.0"
python-dotenv = "^1.0.0"
httpx = "^0.25.0"
aiofiles = "^23.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
black = "^23.0.0"
flake8 = "^6.0.0"
mypy = "^1.7.0"
isort = "^5.12.0"

[tool.poetry.group.test.dependencies]
pytest-cov = "^4.1.0"
httpx = "^0.25.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py39']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### Development Workflow

#### Initial Setup

```bash
# Create project structure
mkdir ai-website-generator
cd ai-website-generator

# Initialize Poetry project
poetry init

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

#### Daily Development

```bash
# Add new dependency
poetry add new-package

# Run application
poetry run uvicorn backend.main:app --reload

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy backend/
```

#### Dependency Management

```bash
# Show current dependencies
poetry show

# Show dependency tree
poetry show --tree

# Check for outdated packages
poetry show --outdated

# Update dependencies
poetry update
```

### Environment Variables

#### .env File Support

```bash
# Install python-dotenv
poetry add python-dotenv
```

```python
# In your application
from dotenv import load_dotenv
import os

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
```

### Scripts and Commands

#### Custom Scripts

```toml
[tool.poetry.scripts]
start = "backend.main:main"
dev = "uvicorn backend.main:app --reload"
test = "pytest"
format = "black ."
lint = "flake8 backend/"
```

Usage:

```bash
poetry run start
poetry run dev
poetry run test
```

### Production Deployment

#### Building for Production

```bash
# Build wheel
poetry build

# Export requirements.txt (if needed)
poetry export -f requirements.txt --output requirements.txt

# Export without dev dependencies
poetry export -f requirements.txt --output requirements.txt --without dev
```

#### Docker Integration

```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Configure Poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --without dev

# Copy application
COPY . .

# Run application
CMD ["poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Best Practices for Our Project

### Dependency Organization

1. **Core Dependencies**: Essential for application runtime
2. **Development Dependencies**: Tools for development (black, pytest, mypy)
3. **Test Dependencies**: Specific to testing environment
4. **Optional Dependencies**: Feature-specific dependencies

### Version Management

1. Use semantic versioning for your project
2. Pin exact versions in poetry.lock
3. Use appropriate constraint operators in pyproject.toml
4. Regular dependency updates with testing

### Virtual Environment

1. Always use Poetry's virtual environment
2. Never install packages globally when working on the project
3. Use `poetry shell` for interactive development
4. Use `poetry run` for script execution

### Security Considerations

1. Regularly update dependencies for security patches
2. Use `poetry audit` (when available) to check for vulnerabilities
3. Review dependency changes before updating
4. Keep poetry.lock in version control

### Performance Tips

1. Use `poetry install --no-dev` in production
2. Cache Poetry dependencies in CI/CD
3. Use `poetry export` for Docker builds when needed
4. Consider using `poetry bundle venv` for deployment
