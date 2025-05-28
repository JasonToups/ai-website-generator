"""UI/UX Designer agent for website design and layout."""

import os
from crewai import Agent
from crewai.tools import BaseTool
from langchain_anthropic import ChatAnthropic


class UIDesignerAgent:
    """UI/UX Designer agent for creating website designs and layouts."""
    
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.3
        )
        
        # Create the agent
        self.agent = Agent(
            role="Senior UI/UX Designer",
            goal="Create beautiful, user-friendly website designs optimized for React and Tailwind CSS",
            backstory="""You are a world-class UI/UX Designer with over 10 years of experience 
            creating stunning web interfaces. You specialize in modern, responsive design using 
            React and Tailwind CSS. You understand design principles, accessibility, user psychology, 
            and current web design trends. You create designs that are not only beautiful but also 
            highly functional and user-friendly. You always consider mobile-first design and ensure 
            excellent user experience across all devices.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
    
    def create_design(self, project_specification: str) -> str:
        """Create a comprehensive UI/UX design based on project specifications."""
        prompt = f"""
        Based on the following project specification, create a comprehensive UI/UX design:
        
        {project_specification}
        
        Create a detailed design specification including:
        
        1. **Design System**:
           - Color palette (primary, secondary, accent colors)
           - Typography scale (headings, body text, captions)
           - Spacing system
           - Border radius and shadows
           - Component variants
        
        2. **Layout Structure**:
           - Header design and navigation
           - Main content areas
           - Sidebar layouts (if needed)
           - Footer design
           - Grid system and breakpoints
        
        3. **Component Specifications**:
           - Buttons (primary, secondary, variants)
           - Forms and input fields
           - Cards and content containers
           - Navigation elements
           - Interactive elements
        
        4. **Responsive Design**:
           - Mobile-first approach
           - Tablet and desktop adaptations
           - Touch-friendly interactions
           - Accessibility considerations
        
        5. **Tailwind CSS Classes**:
           - Specific Tailwind classes for each component
           - Responsive utilities
           - Custom CSS variables if needed
           - Dark mode considerations
        
        6. **User Experience Flow**:
           - User journey mapping
           - Interaction patterns
           - Micro-interactions
           - Loading states and feedback
        
        Focus on modern, clean design that follows current best practices and is optimized 
        for implementation with React and Tailwind CSS. Ensure the design is accessible, 
        performant, and provides excellent user experience.
        """
        
        return self.agent.execute_task(prompt)
