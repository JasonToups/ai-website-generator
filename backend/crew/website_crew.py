"""CrewAI crew for website generation."""

import os
from typing import Dict, Any, List
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool

from backend.agents.product_manager import ProductManagerAgent
from backend.agents.ui_designer import UIDesignerAgent
from backend.agents.software_engineer import SoftwareEngineerAgent
from backend.utils.project_manager import ProjectManager


class WebsiteCrew:
    """CrewAI crew for generating websites."""
    
    def __init__(self):
        self.project_manager = ProjectManager()
        
        # Initialize agents
        self.product_manager = ProductManagerAgent()
        self.ui_designer = UIDesignerAgent()
        self.software_engineer = SoftwareEngineerAgent()
        
        # Create the crew
        self.crew = Crew(
            agents=[
                self.product_manager.agent,
                self.ui_designer.agent,
                self.software_engineer.agent
            ],
            tasks=[],  # Tasks will be created dynamically
            process=Process.sequential,
            verbose=True
        )
    
    async def generate_website(
        self,
        description: str,
        requirements: List[str],
        style_preferences: Dict[str, Any],
        project_id: str
    ) -> Dict[str, Any]:
        """Generate a website using the crew."""
        try:
            # Update status
            self.project_manager.update_project_status(
                project_id, "in_progress", "Creating tasks...", progress=10
            )
            
            # Create tasks for the crew
            tasks = self._create_tasks(description, requirements, style_preferences, project_id)
            self.crew.tasks = tasks
            
            # Update status
            self.project_manager.update_project_status(
                project_id, "in_progress", "Running crew...", progress=20
            )
            
            # Execute the crew
            result = self.crew.kickoff()
            
            # Update status
            self.project_manager.update_project_status(
                project_id, "in_progress", "Processing results...", progress=90
            )
            
            # Process and save results
            self._process_results(result, project_id)
            
            # Final status update
            self.project_manager.update_project_status(
                project_id, "completed", "Website generation completed", progress=100
            )
            
            return {
                "success": True,
                "result": result,
                "project_id": project_id
            }
            
        except Exception as e:
            self.project_manager.add_error(project_id, str(e))
            self.project_manager.update_project_status(
                project_id, "failed", f"Error: {str(e)}"
            )
            return {
                "success": False,
                "error": str(e),
                "project_id": project_id
            }
    
    def _create_tasks(
        self,
        description: str,
        requirements: List[str],
        style_preferences: Dict[str, Any],
        project_id: str
    ) -> List[Task]:
        """Create tasks for the crew."""
        
        # Task 1: Product Manager - Define requirements and structure
        requirements_task = Task(
            description=f"""
            Analyze the website request and create a comprehensive project specification.
            
            Website Description: {description}
            Requirements: {', '.join(requirements) if requirements else 'None specified'}
            Style Preferences: {style_preferences}
            
            Create a detailed specification including:
            1. Project overview and goals
            2. Target audience analysis
            3. Feature requirements
            4. Content structure
            5. Technical specifications
            6. Success criteria
            
            Output should be a structured document that the design and development team can use.
            """,
            agent=self.product_manager.agent,
            expected_output="A comprehensive project specification document"
        )
        
        # Task 2: UI Designer - Create design and layout
        design_task = Task(
            description=f"""
            Based on the project specification, create a complete UI/UX design for the website.
            
            Create:
            1. Wireframes and layout structure
            2. Component specifications
            3. Color scheme and typography
            4. Responsive design guidelines
            5. User experience flow
            6. Tailwind CSS class recommendations
            
            Focus on modern, clean design that follows best practices.
            The design should be implementable with React and Tailwind CSS.
            """,
            agent=self.ui_designer.agent,
            expected_output="Complete UI/UX design specification with component details",
            context=[requirements_task]
        )
        
        # Task 3: Software Engineer - Implement the website
        development_task = Task(
            description=f"""
            Implement the website based on the project specification and design.
            
            CRITICAL REQUIREMENTS - VITE PROJECT:
            - Generate COMPLETE, FUNCTIONAL Vite + React components
            - Every component must have proper opening AND closing tags
            - All imports must be included
            - No truncated or incomplete code
            - If output is getting long, create multiple smaller components instead of truncating
            - MUST use Vite project structure (NOT Create React App)
            - Use modern React Router v6 syntax (Routes, not Switch)
            - Generate main.tsx entry point (not index.js)
            
            Create a complete VITE + React application with:
            1. Component structure following the design
            2. Responsive layout using Tailwind CSS
            3. Clean, maintainable code
            4. Proper file organization for Vite
            5. Modern React patterns (hooks, functional components)
            6. TypeScript for type safety
            7. Modern ES modules and imports
            
            Generate all necessary files with COMPLETE implementations:
            - src/App.tsx (complete main component with modern React Router v6)
            - src/components/Navbar.tsx (complete navigation component)
            - src/components/Hero.tsx (complete hero section)
            - src/components/About.tsx (complete about section)
            - src/components/Contact.tsx (complete contact section)
            - src/components/Footer.tsx (complete footer component)
            - package.json with VITE dependencies (NOT react-scripts):
              * "dev": "vite" script
              * "build": "tsc -b && vite build" script
              * "preview": "vite preview" script
              * Vite, React 19, TypeScript, Tailwind CSS dependencies
            - README.md with Vite setup instructions
            
            IMPORTANT: Each file must be COMPLETE and FUNCTIONAL. Do not cut off mid-component.
            If you need to limit output size, create fewer but complete components rather than incomplete ones.
            
            Project ID for file saving: {project_id}
            """,
            agent=self.software_engineer.agent,
            expected_output="Complete React application with all source files - every component must be fully implemented with proper closing tags",
            context=[requirements_task, design_task]
        )
        
        return [requirements_task, design_task, development_task]
    
    def _process_results(self, result: Any, project_id: str) -> None:
        """Process and save the crew results."""
        try:
            # The result should contain the generated files
            # This is a simplified version - in practice, you'd parse the agent outputs
            # and extract the actual file contents
            
            # For now, save a basic result file
            self.project_manager.save_project_file(
                project_id,
                "crew_output.txt",
                str(result)
            )
            
            # In a real implementation, you would:
            # 1. Parse the software engineer's output to extract React files
            # 2. Save each file to the project directory
            # 3. Create a proper project structure
            
        except Exception as e:
            self.project_manager.add_error(project_id, f"Error processing results: {str(e)}")
