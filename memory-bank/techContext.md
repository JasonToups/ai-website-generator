# Technical Context - AI Website Builder

## Technology Stack

### Backend Technologies

#### Core Framework

- **Python 3.9+**: Primary programming language
- **Poetry**: Dependency management and virtual environment
- **CrewAI**: AI agent orchestration framework
- **FastAPI**: Web framework for REST API endpoints
- **Uvicorn**: ASGI server for FastAPI

#### AI and LLM Integration

- **Anthropic Claude**: Primary LLM for agent intelligence
- **Anthropic SDK**: Official Python client for Claude API
- **Model Context Protocol (MCP)**: Extended capabilities through MCP servers

#### MCP Server Dependencies

- **Filesystem Server**: `@modelcontextprotocol/server-filesystem`
- **Memory Server**: `@modelcontextprotocol/server-memory`
- **Fetch Server**: `@modelcontextprotocol/server-fetch`
- **Sequential Thinking**: `@modelcontextprotocol/server-sequential-thinking`

### Frontend Technologies

#### Core Framework

- **React 18**: UI framework with hooks and functional components
- **TypeScript**: Type safety and enhanced developer experience
- **Vite**: Build tool and development server
- **Node.js 18+**: Runtime environment

#### Styling and UI

- **Tailwind CSS**: Utility-first CSS framework
- **ShadCN/UI**: Modern React component library built on Radix UI and Tailwind CSS
- **Radix UI**: Low-level UI primitives (via ShadCN)
- **Heroicons**: SVG icon library

#### State Management and Data

- **React Built-ins**: useState, useContext, useReducer for state management
- **Axios**: HTTP client for API communication
- **JSON Files**: Simple file-based data storage for MVP

## Development Environment

### Poetry Configuration

```toml
[tool.poetry]
name = "ai-website-generator"
version = "0.1.0"
description = "AI-powered website builder using CrewAI"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
crewai = "^0.1.0"
fastapi = "^0.104.0"
uvicorn = "^0.24.0"
anthropic = "^0.7.0"
pydantic = "^2.5.0"
python-dotenv = "^1.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.0.0"
flake8 = "^6.0.0"
mypy = "^1.7.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Environment Variables

```bash
# .env file structure
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Project Structure

```
ai-website-generator/
├── pyproject.toml              # Poetry configuration
├── .env                        # Environment variables
├── .gitignore                  # Git ignore patterns
├── README.md                   # Project documentation
├── backend/                    # Python backend
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Configuration management
│   ├── agents/                 # CrewAI agents
│   │   ├── __init__.py
│   │   ├── base_agent.py       # Base agent class
│   │   ├── product_manager.py  # Product Manager agent
│   │   ├── ui_designer.py      # UI/UX Designer agent
│   │   └── software_engineer.py # Software Engineer agent
│   ├── crew/                   # CrewAI crew management
│   │   ├── __init__.py
│   │   ├── website_crew.py     # Main crew orchestration
│   │   └── tasks.py            # Task definitions
│   ├── api/                    # FastAPI routes
│   │   ├── __init__.py
│   │   ├── routes.py           # API endpoints
│   │   └── models.py           # Pydantic models
│   ├── mcp/                    # MCP server integration
│   │   ├── __init__.py
│   │   ├── client.py           # MCP client wrapper
│   │   └── servers.py          # Server configuration
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── file_operations.py  # File handling
│       └── logging.py          # Logging configuration
├── frontend/                   # React frontend
│   ├── package.json            # NPM dependencies
│   ├── tsconfig.json           # TypeScript configuration
│   ├── tailwind.config.js      # Tailwind configuration
│   ├── vite.config.ts          # Vite configuration
│   ├── src/
│   │   ├── main.tsx            # Application entry point
│   │   ├── App.tsx             # Root component
│   │   ├── components/         # React components
│   │   │   ├── ui/             # Base UI components
│   │   │   ├── forms/          # Form components
│   │   │   └── preview/        # Preview components
│   │   ├── pages/              # Page components
│   │   ├── hooks/              # Custom React hooks
│   │   ├── services/           # API service functions
│   │   ├── types/              # TypeScript type definitions
│   │   └── utils/              # Utility functions
│   └── public/                 # Static assets
├── generated/                  # Generated project outputs
│   └── projects/               # Individual generated projects
└── memory-bank/                # Project documentation
    ├── projectbrief.md
    ├── productContext.md
    ├── systemPatterns.md
    ├── techContext.md
    ├── activeContext.md
    ├── progress.md
    └── official-documentation/
```

## API Design

### REST Endpoints

```python
# API endpoint structure
POST /api/projects/generate     # Start project generation
GET  /api/projects/{id}/status  # Check generation status
GET  /api/projects/{id}/files   # Get generated files
POST /api/projects/{id}/iterate # Request modifications
GET  /api/projects              # List user projects
DELETE /api/projects/{id}       # Delete project
```

### Request/Response Models

```python
# Pydantic models for API
class ProjectRequest(BaseModel):
    name: str
    description: str
    requirements: List[str]
    style_preferences: Optional[Dict[str, Any]]

class ProjectResponse(BaseModel):
    id: str
    status: str
    progress: float
    files: Optional[List[GeneratedFile]]
    errors: Optional[List[str]]
```

## Development Workflow

### Setup Commands

```bash
# Backend setup
poetry install
poetry shell
poetry run uvicorn backend.main:app --reload

# Frontend setup
cd frontend
npm install
npm run dev

# MCP server setup (if needed locally)
npx @modelcontextprotocol/server-filesystem
npx @modelcontextprotocol/server-memory
```

### Testing Strategy

```python
# Testing approach
- Unit tests for individual agents
- Integration tests for crew collaboration
- API endpoint testing with FastAPI TestClient
- Frontend component testing with React Testing Library
- End-to-end testing with Playwright
```

## Deployment Considerations

### Production Environment

- **Backend**: Docker container with Poetry
- **Frontend**: Static build deployed to CDN
- **Database**: PostgreSQL for project persistence
- **File Storage**: S3-compatible storage for generated files
- **Monitoring**: Application performance monitoring

### Security Requirements

- API key encryption and rotation
- Input validation and sanitization
- Rate limiting on API endpoints
- CORS configuration for frontend
- Generated code safety validation

## Performance Optimization

### Backend Optimization

- Async/await for I/O operations
- Connection pooling for database
- Caching for frequent operations
- Background tasks for long-running generation

### Frontend Optimization

- Code splitting and lazy loading
- Component memoization
- Optimized bundle size
- Progressive loading for large projects

## Monitoring and Logging

### Logging Strategy

```python
# Structured logging approach
import logging
import structlog

# Configure structured logging
logging.basicConfig(level=logging.INFO)
logger = structlog.get_logger()

# Usage in agents
logger.info("Agent started", agent_type="product_manager", task_id="123")
```

### Metrics to Track

- Generation success rate
- Average generation time
- Agent collaboration efficiency
- User satisfaction scores
- System resource usage

## Integration Points

### CrewAI Integration

```python
# CrewAI agent configuration
from crewai import Agent, Task, Crew

agent = Agent(
    role="Product Manager",
    goal="Analyze requirements and create project specifications",
    backstory="Expert in product management and requirement analysis",
    tools=[memory_tool, sequential_thinking_tool]
)
```

### MCP Server Integration

```python
# MCP client configuration
from mcp import Client

mcp_client = Client()
await mcp_client.connect("filesystem", "npx @modelcontextprotocol/server-filesystem")
```

## Quality Assurance

### Code Quality Tools

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing framework
- **ESLint**: Frontend linting
- **Prettier**: Frontend formatting

### Best Practices

- Type hints for all Python functions
- Comprehensive error handling
- Consistent naming conventions
- Documentation for all public APIs
- Regular dependency updates
