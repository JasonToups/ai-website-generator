# AI Website Builder with CrewAI - Project Brief

## Project Overview

An intelligent website generator that uses a team of AI agents to collaboratively create React applications with Tailwind styling. The system leverages CrewAI's orchestration framework to coordinate three specialized agents working together to transform user requirements into complete, functional React projects.

## Core Requirements

### Primary Objective

Build an AI-powered website generator that can create React applications through collaborative AI agents, each with specialized roles and capabilities.

### Key Components

1. **Three AI Agents**:

   - Product Manager Agent (requirements analysis)
   - UI/UX Designer Agent (design and user experience)
   - Software Engineer Agent (code implementation)

2. **Technology Stack**:

   - Backend: Python with CrewAI framework
   - Frontend: React with Tailwind CSS and ShadCN/UI components
   - LLM: Anthropic Claude
   - Environment: Poetry for Python dependency management
   - Enhancement: MCP servers for extended capabilities

3. **Output**: React applications styled with Tailwind CSS and ShadCN/UI components (no backends initially)

## Success Criteria

- Agents can collaborate effectively to generate complete React projects
- User can input requirements through an intuitive React frontend
- Generated code follows best practices and is production-ready
- System can handle iterative refinement based on user feedback
- Projects are downloadable and immediately runnable

## Constraints

- Focus on frontend React applications only (no backend generation initially)
- Use Tailwind CSS for all styling
- Maintain security through proper environment variable management
- Ensure scalable architecture for future enhancements

## Future Considerations

- Potential backend generation capabilities
- Integration with version control systems
- Template library expansion
- Advanced customization options
