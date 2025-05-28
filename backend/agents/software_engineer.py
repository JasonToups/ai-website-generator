"""Software Engineer agent for React application development."""

import os
from crewai import Agent
from crewai.tools import BaseTool
from langchain_anthropic import ChatAnthropic


class SoftwareEngineerAgent:
    """Software Engineer agent for implementing React applications."""
    
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.2
        )
        
        # Create the agent
        self.agent = Agent(
            role="Senior Full-Stack Developer",
            goal="Implement high-quality React applications with TypeScript and Tailwind CSS",
            backstory="""You are an expert Full-Stack Developer with 8+ years of experience 
            building modern web applications. You specialize in React, TypeScript, and Tailwind CSS. 
            You write clean, maintainable, and performant code following best practices. You understand 
            modern React patterns, hooks, component composition, and state management. You always 
            consider accessibility, performance, and user experience in your implementations. You 
            create well-structured, scalable applications with proper error handling and testing.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
    
    def implement_website(self, project_specification: str, design_specification: str) -> str:
        """Implement a complete React website based on specifications."""
        prompt = f"""
        Implement a complete React application based on the following specifications:
        
        PROJECT SPECIFICATION:
        {project_specification}
        
        DESIGN SPECIFICATION:
        {design_specification}
        
        Create a complete React application with the following requirements:
        
        1. **Project Structure**:
           - Modern React with TypeScript
           - Functional components with hooks
           - Proper file organization
           - Component-based architecture
        
        2. **Implementation Requirements**:
           - Responsive design using Tailwind CSS
           - Accessible HTML structure
           - Modern React patterns (hooks, context if needed)
           - Clean, readable code with proper TypeScript types
           - Error boundaries and loading states
        
        3. **Files to Generate**:
           - package.json with all necessary dependencies
           - tsconfig.json for TypeScript configuration
           - tailwind.config.js for Tailwind customization
           - src/App.tsx (main application component)
           - src/components/ (all UI components)
           - src/types/ (TypeScript type definitions)
           - src/utils/ (utility functions if needed)
           - README.md with setup and run instructions
        
        4. **Code Quality**:
           - Follow React best practices
           - Use semantic HTML elements
           - Implement proper TypeScript typing
           - Include JSDoc comments for complex functions
           - Ensure mobile-first responsive design
           - Follow accessibility guidelines (WCAG)
        
        5. **Styling**:
           - Use Tailwind CSS classes exclusively
           - Implement the design system from specifications
           - Ensure consistent spacing and typography
           - Include hover states and transitions
           - Support dark mode if specified
        
        For each file, provide the complete code with proper formatting. Start each file 
        with a comment indicating the file path (e.g., // src/App.tsx).
        
        Generate production-ready code that can be immediately used to create a working website.
        """
        
        return self.agent.execute_task(prompt)
