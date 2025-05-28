"""Project management utilities for tracking website generation projects."""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


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
