# AI Website Generator

A CrewAI-powered website builder that uses a team of AI agents (Product Manager, UI/UX Designer, and Software Engineer) to generate React applications with Tailwind CSS.

## 🚀 Quick Start

```bash
# Complete setup and start development
make setup
make dev
```

That's it! The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:5173`.

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- Poetry (for Python dependency management)
- An Anthropic API key

## 🛠️ Installation

### Option 1: Using Makefile (Recommended)

```bash
# Install all dependencies
make install

# Create .env file and complete setup
make setup

# Start development servers
make dev
```

### Option 2: Manual Installation

1. **Install backend dependencies:**

   ```bash
   poetry install
   ```

2. **Install frontend dependencies:**

   ```bash
   cd frontend
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

## 🔧 Configuration

Add your Anthropic API key to the `.env` file:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## 🎯 Usage

### Development

```bash
# Start both backend and frontend
make dev

# Start only backend
make backend

# Start only frontend
make frontend
```

### Testing & Quality

```bash
# Run all tests
make test

# Lint code
make lint

# Format code
make format
```

### Production

```bash
# Build for production
make build

# Start production server
make start
```

## 📁 Project Structure

```
ai-website-generator/
├── backend/                 # FastAPI backend
│   ├── agents/             # CrewAI agents
│   │   ├── product_manager.py
│   │   ├── ui_designer.py
│   │   └── software_engineer.py
│   ├── api/                # API routes
│   ├── crew/               # CrewAI crew configuration
│   ├── mcp/                # MCP server integrations
│   └── utils/              # Utility functions
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   └── lib/           # Utilities
│   └── public/
├── generated/              # Generated websites
├── data/                   # Project data storage
├── memory-bank/           # AI memory and documentation
└── Makefile              # Development commands
```

## 🤖 How It Works

1. **Product Manager Agent**: Analyzes requirements and creates project specifications
2. **UI/UX Designer Agent**: Creates design systems and component specifications
3. **Software Engineer Agent**: Implements the React application with TypeScript and Tailwind CSS

The agents work together in sequence to deliver a complete, production-ready website.

## 🌐 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/v1/generate` - Start website generation
- `GET /api/v1/projects/{id}/status` - Get project status
- `GET /api/v1/projects` - List all projects
- `GET /api/v1/projects/{id}/files` - Get generated files

## 📖 Available Make Commands

Run `make help` to see all available commands:

### Setup & Installation

- `make setup` - Complete project setup
- `make install` - Install all dependencies

### Development

- `make dev` - Start both servers
- `make backend` - Start FastAPI server
- `make frontend` - Start React server

### Testing & Quality

- `make test` - Run all tests
- `make lint` - Lint code
- `make format` - Format code

### Production

- `make build` - Build for production
- `make start` - Start production server

### Utilities

- `make clean` - Clean build artifacts
- `make reset` - Reset project state
- `make logs` - Show application logs
- `make health` - Check application health
- `make status` - Show project status

## 🔍 Development Workflow

1. **Start development:**

   ```bash
   make dev
   ```

2. **Make changes to code**

3. **Test and lint:**

   ```bash
   make quick-test
   ```

4. **Generate a website:**
   - Open `http://localhost:5173`
   - Enter website description and requirements
   - Watch the AI agents work together

## 🚀 Deployment

```bash
# Prepare for deployment
make deploy-prep

# Build production assets
make build

# Start production server
make start
```

## 🧪 Testing

The project includes comprehensive testing:

- **Backend**: pytest with async support
- **Frontend**: Vitest with React Testing Library
- **Linting**: flake8, mypy, ESLint
- **Formatting**: black, isort, Prettier

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make quick-test`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Backend won't start:**

- Check that your `ANTHROPIC_API_KEY` is set in `.env`
- Ensure Poetry dependencies are installed: `make install`

**Frontend won't start:**

- Check Node.js version (18+ required)
- Clear cache: `make clean && make install`

**Generation fails:**

- Verify API key is valid
- Check backend logs: `make logs`
- Ensure all agents are properly configured

### Getting Help

- Check the logs: `make logs`
- Verify health: `make health`
- Reset project: `make reset`

For more help, check the memory-bank documentation or create an issue.
