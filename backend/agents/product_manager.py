"""Product Manager agent for website requirements analysis."""

import os
from crewai import Agent
from crewai.tools import BaseTool
from langchain_anthropic import ChatAnthropic


class ProductManagerAgent:
    """Product Manager agent for analyzing requirements and creating specifications."""
    
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.1
        )
        
        # Create the agent
        self.agent = Agent(
            role="Senior Product Manager",
            goal="Analyze website requirements and create comprehensive project specifications",
            backstory="""You are an experienced Product Manager with expertise in web development 
            and user experience. You excel at understanding client needs, defining clear requirements, 
            and creating detailed specifications that guide design and development teams. You have 
            worked on hundreds of web projects and understand what makes websites successful.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
    
    def analyze_requirements(self, description: str, requirements: list, style_preferences: dict) -> str:
        """Analyze and structure the website requirements."""
        prompt = f"""
        Analyze the following website request and create a comprehensive project specification:
        
        Description: {description}
        Requirements: {requirements}
        Style Preferences: {style_preferences}
        
        Create a detailed specification including:
        1. Project Overview and Goals
        2. Target Audience Analysis
        3. Feature Requirements (prioritized)
        4. Content Structure and Sitemap
        5. Technical Requirements
        6. Success Criteria and KPIs
        7. Timeline and Milestones
        
        Format the output as a structured document that can guide the design and development process.
        """
        
        return self.agent.execute_task(prompt)
