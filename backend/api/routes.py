"""API routes for the AI Website Generator."""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from backend.crew.website_crew import WebsiteCrew
from backend.utils.project_manager import ProjectManager

router = APIRouter()

# Pydantic models for request/response
class WebsiteRequest(BaseModel):
    """Request model for website generation."""
    description: str = Field(..., description="Description of the website to build")
    requirements: List[str] = Field(default=[], description="Specific requirements")
    style_preferences: Dict[str, Any] = Field(default={}, description="Style preferences")

class WebsiteResponse(BaseModel):
    """Response model for website generation."""
    project_id: str = Field(..., description="Unique project identifier")
    status: str = Field(..., description="Generation status")
    message: str = Field(..., description="Status message")

class ProjectStatus(BaseModel):
    """Project status model."""
    project_id: str
    status: str
    progress: int
    current_step: str
    files_generated: List[str]
    errors: List[str]


@router.post("/generate", response_model=WebsiteResponse)
async def generate_website(
    request: WebsiteRequest,
    background_tasks: BackgroundTasks
) -> WebsiteResponse:
    """Generate a website using the CrewAI team."""
    try:
        # Create project manager
        project_manager = ProjectManager()
        project_id = project_manager.create_project(
            description=request.description,
            requirements=request.requirements,
            style_preferences=request.style_preferences
        )
        
        # Start website generation in background
        background_tasks.add_task(
            _generate_website_task,
            project_id,
            request.description,
            request.requirements,
            request.style_preferences
        )
        
        return WebsiteResponse(
            project_id=project_id,
            status="started",
            message="Website generation started. Check status for progress."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start generation: {str(e)}")


@router.get("/projects/{project_id}/status", response_model=ProjectStatus)
async def get_project_status(project_id: str) -> ProjectStatus:
    """Get the status of a website generation project."""
    try:
        project_manager = ProjectManager()
        status = project_manager.get_project_status(project_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Project not found")
            
        return ProjectStatus(**status)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.get("/projects")
async def list_projects() -> Dict[str, Any]:
    """List all projects."""
    try:
        project_manager = ProjectManager()
        projects = project_manager.list_projects()
        
        return {
            "projects": projects,
            "total": len(projects)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list projects: {str(e)}")


@router.get("/projects/{project_id}/files")
async def get_project_files(project_id: str) -> Dict[str, Any]:
    """Get the generated files for a project."""
    try:
        project_manager = ProjectManager()
        files = project_manager.get_project_files(project_id)
        
        if files is None:
            raise HTTPException(status_code=404, detail="Project not found")
            
        return {
            "project_id": project_id,
            "files": files
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get files: {str(e)}")


async def _generate_website_task(
    project_id: str,
    description: str,
    requirements: List[str],
    style_preferences: Dict[str, Any]
) -> None:
    """Background task to generate website."""
    try:
        # Initialize the website crew
        crew = WebsiteCrew()
        
        # Update project status
        project_manager = ProjectManager()
        project_manager.update_project_status(project_id, "in_progress", "Initializing crew...")
        
        # Run the crew
        result = await crew.generate_website(
            description=description,
            requirements=requirements,
            style_preferences=style_preferences,
            project_id=project_id
        )
        
        # Update final status
        if result.get("success"):
            project_manager.update_project_status(
                project_id, 
                "completed", 
                "Website generation completed successfully"
            )
        else:
            project_manager.update_project_status(
                project_id, 
                "failed", 
                f"Generation failed: {result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        # Update error status
        project_manager = ProjectManager()
        project_manager.update_project_status(
            project_id, 
            "failed", 
            f"Generation failed: {str(e)}"
        )
