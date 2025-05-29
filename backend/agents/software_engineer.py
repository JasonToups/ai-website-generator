"""Software Engineer agent for React application development."""

import os
from crewai import Agent
from langchain_anthropic import ChatAnthropic


class SoftwareEngineerAgent:
    """Software Engineer agent for implementing React applications."""
    
    def __init__(self):
        # Initialize the LLM with maximum allowed tokens for Claude 3 Sonnet
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.2,
            max_tokens=4096  # Maximum allowed for Claude 3 Sonnet
        )
        
        # Create the agent
        self.agent = Agent(
            role="Senior Full-Stack Developer",
            goal="Implement complete, production-ready React applications with TypeScript and Tailwind CSS. Always generate COMPLETE files with proper closing tags and full implementations.",
            backstory="""You are an expert Full-Stack Developer with 8+ years of experience 
            building modern web applications. You specialize in React, TypeScript, and Tailwind CSS. 
            You write clean, maintainable, and performant code following best practices. You understand 
            modern React patterns, hooks, component composition, and state management. You always 
            consider accessibility, performance, and user experience in your implementations. You 
            create well-structured, scalable applications with proper error handling and testing.
            
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
