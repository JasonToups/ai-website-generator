"""API routes for the AI Website Generator."""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from backend.crew.website_crew import WebsiteCrew
from backend.utils.project_manager import ProjectManager
from backend.utils.project_structure import ProjectStructureManager
from backend.utils.file_parser import ProjectFileParser

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
        
        # Map 'id' field to 'project_id' for the response model
        status_data = status.copy()
        status_data['project_id'] = status_data.pop('id')
            
        return ProjectStatus(**status_data)
        
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


# ========================================
# PHASE 3: NEW FILE OPERATION ENDPOINTS
# ========================================

@router.get("/projects/{project_id}/files/tree")
async def get_project_file_tree(project_id: str) -> Dict[str, Any]:
    """Get hierarchical file tree structure for a project."""
    try:
        manager = ProjectStructureManager(project_id)
        result = manager.get_file_tree()
        
        if not result['success']:
            raise HTTPException(status_code=404, detail=result.get('error', 'Project files not found'))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file tree: {str(e)}")


@router.get("/projects/{project_id}/files/{file_path:path}")
async def get_project_file(project_id: str, file_path: str) -> Dict[str, Any]:
    """Get individual file content with metadata."""
    try:
        manager = ProjectStructureManager(project_id)
        result = manager.get_individual_file(file_path)
        
        if not result['success']:
            raise HTTPException(status_code=404, detail=result.get('error', 'File not found'))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file: {str(e)}")


@router.get("/projects/{project_id}/download")
async def download_project_zip(project_id: str):
    """Download complete project as ZIP archive."""
    try:
        manager = ProjectStructureManager(project_id)
        zip_path = manager.project_path / "project.zip"
        
        # Generate ZIP if it doesn't exist
        if not zip_path.exists():
            zip_result = manager.create_zip_archive()
            if not zip_result['success']:
                raise HTTPException(status_code=500, detail="ZIP generation failed")
        
        # Return file for download
        return FileResponse(
            path=str(zip_path),
            filename=f"project-{project_id}.zip",
            media_type="application/zip"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download project: {str(e)}")


@router.get("/projects/{project_id}/preview")
async def get_project_preview(project_id: str) -> Dict[str, Any]:
    """Get live preview information for a project (Phase 3 foundation)."""
    try:
        manager = ProjectStructureManager(project_id)
        
        # Check if project files exist
        if not manager.files_path.exists():
            raise HTTPException(status_code=404, detail="Project files not found")
        
        # For now, return preview readiness info
        # TODO: Implement ProjectPreviewManager in next step
        return {
            "success": True,
            "project_id": project_id,
            "preview_ready": True,
            "files_path": str(manager.files_path),
            "message": "Preview infrastructure ready - ProjectPreviewManager to be implemented",
            "status": "foundation_ready"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get preview info: {str(e)}")


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
            # PHASE 3 ENHANCEMENT: Add automatic file parsing
            try:
                # Get the crew output for parsing
                crew_output = result.get("output", "")
                if crew_output:
                    # Parse files and create structure
                    parser = ProjectFileParser(crew_output, project_id)
                    parsed_result = parser.parse()
                    
                    if parsed_result['success']:
                        # Create project structure
                        from backend.utils.project_structure import create_project_structure
                        structure_result = create_project_structure(project_id, parsed_result)
                        
                        if structure_result['success']:
                            project_manager.update_project_status(
                                project_id, 
                                "completed", 
                                f"Website generation completed successfully. {structure_result['total_files']} files created."
                            )
                        else:
                            project_manager.update_project_status(
                                project_id, 
                                "completed", 
                                "Website generation completed. File parsing encountered issues."
                            )
                    else:
                        project_manager.update_project_status(
                            project_id, 
                            "completed", 
                            "Website generation completed. File parsing failed."
                        )
                else:
                    project_manager.update_project_status(
                        project_id, 
                        "completed", 
                        "Website generation completed successfully"
                    )
            except Exception as parse_error:
                # Don't fail the entire generation if parsing fails
                project_manager.update_project_status(
                    project_id, 
                    "completed", 
                    f"Website generation completed. File parsing error: {str(parse_error)}"
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
