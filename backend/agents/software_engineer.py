"""Software Engineer agent for React application development."""

import os
from crewai import Agent
from langchain_anthropic import ChatAnthropic


class SoftwareEngineerAgent:
    """Software Engineer agent for implementing React applications."""
    
    def __init__(self):
        # Initialize the LLM with Claude 3.5 Sonnet for better code generation
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.2,
            max_tokens=8192  # Claude 3.5 Sonnet supports higher token limits
        )
        
        # Create the agent
        self.agent = Agent(
            role="Senior Full-Stack Developer",
            goal="Implement complete, production-ready Vite + React applications with TypeScript and Tailwind CSS. Always generate COMPLETE files with proper closing tags and full implementations.",
            backstory="""You are an expert Full-Stack Developer with 8+ years of experience 
            building modern web applications using Vite, React, TypeScript, and Tailwind CSS. 
            You specialize in modern development tooling and write clean, maintainable, and performant code 
            following best practices. You understand modern React patterns, hooks, component composition, 
            and state management. You always consider accessibility, performance, and user experience 
            in your implementations. You create well-structured, scalable applications with proper 
            error handling and testing.
            
            VITE EXPERTISE: You are an expert with Vite and always generate Vite-compatible projects:
            - Use modern ES modules and imports
            - Generate proper main.tsx entry points (not index.js)
            - Use modern React Router v6 syntax (Routes, not Switch)
            - Create Vite-compatible package.json with "vite dev" scripts
            - Use proper TypeScript configurations for Vite
            - Never use Create React App patterns or react-scripts
            
            CRITICAL: You ALWAYS generate COMPLETE files. You never truncate or cut off code mid-way.
            Every component must be fully implemented with proper opening and closing tags, complete
            function implementations, and all necessary imports. If a file is getting long, you break
            it into smaller, focused components rather than truncating the output.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            max_iter=3,  # Allow multiple iterations if needed
            max_execution_time=300  # 5 minutes timeout
        )
