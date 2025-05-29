"""Project management utilities for tracking website generation projects."""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from backend.utils.project_structure import ProjectStructureManager
from backend.utils.project_preview import preview_manager


class ProjectManager:
    """Manages website generation projects and their status."""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.projects_dir = Path("generated/projects")
        self.data_dir.mkdir(exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.projects_file = self.data_dir / "projects.json"
        
        # Initialize projects file if it doesn't exist
        if not self.projects_file.exists():
            self._save_projects({})
    
    def create_project(
        self,
        description: str,
        requirements: List[str],
        style_preferences: Dict[str, Any]
    ) -> str:
        """Create a new project and return its ID."""
        project_id = str(uuid.uuid4())
        
        project_data = {
            "id": project_id,
            "description": description,
            "requirements": requirements,
            "style_preferences": style_preferences,
            "status": "created",
            "progress": 0,
            "current_step": "Initializing...",
            "files_generated": [],
            "errors": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save project data
        projects = self._load_projects()
        projects[project_id] = project_data
        self._save_projects(projects)
        
        # Create project directory
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        return project_id
    
    def get_project_status(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a project."""
        projects = self._load_projects()
        return projects.get(project_id)
    
    def update_project_status(
        self,
        project_id: str,
        status: str,
        current_step: str,
        progress: Optional[int] = None,
        files_generated: Optional[List[str]] = None,
        errors: Optional[List[str]] = None
    ) -> None:
        """Update project status."""
        projects = self._load_projects()
        
        if project_id not in projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = projects[project_id]
        project["status"] = status
        project["current_step"] = current_step
        project["updated_at"] = datetime.now().isoformat()
        
        if progress is not None:
            project["progress"] = progress
        
        if files_generated is not None:
            project["files_generated"] = files_generated
        
        if errors is not None:
            project["errors"] = errors
        
        self._save_projects(projects)
    
    def add_generated_file(self, project_id: str, file_path: str) -> None:
        """Add a generated file to the project."""
        projects = self._load_projects()
        
        if project_id not in projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = projects[project_id]
        if file_path not in project["files_generated"]:
            project["files_generated"].append(file_path)
            project["updated_at"] = datetime.now().isoformat()
            self._save_projects(projects)
    
    def add_error(self, project_id: str, error: str) -> None:
        """Add an error to the project."""
        projects = self._load_projects()
        
        if project_id not in projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = projects[project_id]
        project["errors"].append({
            "message": error,
            "timestamp": datetime.now().isoformat()
        })
        project["updated_at"] = datetime.now().isoformat()
        self._save_projects(projects)
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects."""
        projects = self._load_projects()
        return list(projects.values())
    
    def get_project_files(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get the generated files for a project."""
        project_dir = self.projects_dir / project_id
        
        if not project_dir.exists():
            return None
        
        files = {}
        for file_path in project_dir.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(project_dir)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        files[str(relative_path)] = f.read()
                except Exception as e:
                    files[str(relative_path)] = f"Error reading file: {str(e)}"
        
        return files
    
    def save_project_file(
        self,
        project_id: str,
        file_path: str,
        content: str
    ) -> None:
        """Save a file to the project directory."""
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        full_path = project_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Add to generated files list
        self.add_generated_file(project_id, file_path)
    
    # ========================================
    # PHASE 5: GALLERY METHODS
    # ========================================
    
    def get_gallery_projects(self) -> List[Dict[str, Any]]:
        """Get all projects with enhanced metadata for gallery display."""
        projects = self._load_projects()
        gallery_projects = []
        
        for project_id, project_data in projects.items():
            # Get enhanced metadata
            metadata = self._get_project_metadata(project_id)
            
            # Create gallery project entry
            gallery_project = {
                "project_id": project_id,
                "title": self._generate_project_title(project_data["description"]),
                "description": project_data["description"],
                "status": project_data["status"],
                "created_at": project_data["created_at"],
                "updated_at": project_data["updated_at"],
                "file_count": metadata["file_count"],
                "has_preview": metadata["has_preview"],
                "thumbnail_url": metadata["thumbnail_url"],
                "preview_url": metadata["preview_url"],
                "download_url": f"/api/v1/projects/{project_id}/download",
                "metadata": {
                    "website_type": metadata["website_type"],
                    "technologies": metadata["technologies"],
                    "file_size": metadata["file_size"]
                }
            }
            
            gallery_projects.append(gallery_project)
        
        # Sort by creation date (newest first)
        gallery_projects.sort(key=lambda x: x["created_at"], reverse=True)
        
        return gallery_projects
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project and all its associated files."""
        try:
            # Remove from projects data
            projects = self._load_projects()
            if project_id not in projects:
                return False
            
            del projects[project_id]
            self._save_projects(projects)
            
            # Remove project directory
            project_dir = self.projects_dir / project_id
            if project_dir.exists():
                import shutil
                shutil.rmtree(project_dir)
            
            # Stop any running preview
            try:
                preview_manager.stop_preview(project_id)
            except:
                pass  # Ignore errors if preview wasn't running
            
            return True
            
        except Exception as e:
            print(f"Error deleting project {project_id}: {str(e)}")
            return False
    
    def _get_project_metadata(self, project_id: str) -> Dict[str, Any]:
        """Extract metadata for a project."""
        project_dir = self.projects_dir / project_id
        files_dir = project_dir / "files"
        
        metadata = {
            "file_count": 0,
            "has_preview": False,
            "thumbnail_url": None,
            "preview_url": None,
            "website_type": "Unknown",
            "technologies": [],
            "file_size": 0
        }
        
        # Check if files exist
        if not files_dir.exists():
            return metadata
        
        # Count files and calculate size
        file_count = 0
        total_size = 0
        technologies = set()
        
        for file_path in files_dir.rglob("*"):
            if file_path.is_file():
                file_count += 1
                total_size += file_path.stat().st_size
                
                # Detect technologies from file extensions
                suffix = file_path.suffix.lower()
                if suffix == '.tsx':
                    technologies.add('React')
                    technologies.add('TypeScript')
                elif suffix == '.ts':
                    technologies.add('TypeScript')
                elif suffix == '.jsx':
                    technologies.add('React')
                elif suffix == '.js':
                    technologies.add('JavaScript')
                elif suffix == '.css':
                    technologies.add('CSS')
                elif suffix == '.html':
                    technologies.add('HTML')
                elif suffix == '.json':
                    if file_path.name == 'package.json':
                        technologies.add('Node.js')
        
        metadata["file_count"] = file_count
        metadata["file_size"] = total_size
        metadata["technologies"] = list(technologies)
        
        # Determine website type
        if 'React' in technologies:
            metadata["website_type"] = "React Application"
        elif 'HTML' in technologies:
            metadata["website_type"] = "Static Website"
        else:
            metadata["website_type"] = "Web Project"
        
        # Check if preview is available
        if files_dir.exists() and file_count > 0:
            metadata["has_preview"] = True
            # Check if preview is currently running
            preview_url = preview_manager.get_preview_url(project_id)
            if preview_url:
                metadata["preview_url"] = preview_url
        
        # TODO: Add thumbnail generation in future
        # For now, use a placeholder or default thumbnail
        metadata["thumbnail_url"] = f"/api/v1/projects/{project_id}/thumbnail"
        
        return metadata
    
    def _generate_project_title(self, description: str) -> str:
        """Generate a user-friendly title from project description."""
        # Take first 50 characters and clean up
        title = description[:50].strip()
        
        # Capitalize first letter
        if title:
            title = title[0].upper() + title[1:]
        
        # Add ellipsis if truncated
        if len(description) > 50:
            title += "..."
        
        return title or "Untitled Project"
    
    def _load_projects(self) -> Dict[str, Any]:
        """Load projects from file."""
        try:
            with open(self.projects_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_projects(self, projects: Dict[str, Any]) -> None:
        """Save projects to file."""
        with open(self.projects_file, 'w') as f:
            json.dump(projects, f, indent=2)
