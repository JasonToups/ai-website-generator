"""Project structure manager for creating physical file structures and ZIP archives."""

import os
import zipfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

# Import template injection functionality
try:
    from .template_engine import inject_templates
except ImportError:
    # Fallback if template_engine is not available
    def inject_templates(parsed_files, project_metadata):
        return parsed_files


class ProjectStructureManager:
    """Manage project folder structure and file creation."""
    
    def __init__(self, project_id: str, base_path: str = "generated/projects"):
        self.project_id = project_id
        self.base_path = Path(base_path)
        self.project_path = self.base_path / project_id
        self.files_path = self.project_path / "files"
        self.zip_path = self.project_path / "project.zip"
        
    def create_project_folder(self, parsed_files: Dict[str, Any]) -> Dict[str, Any]:
        """Create physical folder structure with individual files."""
        try:
            # Ensure project directories exist
            self.files_path.mkdir(parents=True, exist_ok=True)
            
            created_files = []
            created_directories = set()
            
            # Create all files
            for file_path, file_info in parsed_files['files'].items():
                full_file_path = self.files_path / file_path
                
                # Create directory if it doesn't exist
                directory = full_file_path.parent
                if directory != self.files_path:
                    directory.mkdir(parents=True, exist_ok=True)
                    created_directories.add(str(directory.relative_to(self.files_path)))
                
                # Write file content
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info['content'])
                
                created_files.append({
                    'path': file_path,
                    'full_path': str(full_file_path),
                    'size': file_info['size'],
                    'is_valid': file_info.get('is_valid', True),
                    'template_generated': file_info.get('template_generated', False)
                })
            
            # Create file manifest - convert set to list for JSON serialization
            manifest = self._create_file_manifest(parsed_files, created_files, list(created_directories))
            manifest_path = self.project_path / "parsed_files.json"
            
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
            
            return {
                'success': True,
                'project_path': str(self.project_path),
                'files_path': str(self.files_path),
                'created_files': created_files,
                'created_directories': list(created_directories),
                'manifest_path': str(manifest_path),
                'total_files': len(created_files),
                'total_directories': len(created_directories),
                'templates_injected': parsed_files.get('metadata', {}).get('templates_injected', 0)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'project_path': str(self.project_path),
                'files_path': str(self.files_path)
            }
    
    def create_zip_archive(self) -> Dict[str, Any]:
        """Create downloadable ZIP archive of the project."""
        try:
            if not self.files_path.exists():
                return {
                    'success': False,
                    'error': 'Project files directory does not exist',
                    'zip_path': str(self.zip_path)
                }
            
            # Create ZIP archive
            with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add all files from the files directory
                for file_path in self.files_path.rglob('*'):
                    if file_path.is_file():
                        # Calculate relative path for ZIP
                        arcname = file_path.relative_to(self.files_path)
                        zipf.write(file_path, arcname)
            
            # Get ZIP file info
            zip_size = self.zip_path.stat().st_size
            
            return {
                'success': True,
                'zip_path': str(self.zip_path),
                'zip_size': zip_size,
                'zip_size_mb': round(zip_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'zip_path': str(self.zip_path)
            }
    
    def get_file_tree(self) -> Dict[str, Any]:
        """Get project file tree for frontend display."""
        try:
            if not self.files_path.exists():
                return {
                    'success': False,
                    'error': 'Project files directory does not exist'
                }
            
            tree = self._build_file_tree(self.files_path)
            
            return {
                'success': True,
                'tree': tree,
                'total_files': self._count_files_in_tree(tree),
                'total_size': self._calculate_tree_size(tree)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_individual_file(self, file_path: str) -> Dict[str, Any]:
        """Get individual file content and metadata."""
        try:
            full_path = self.files_path / file_path
            
            if not full_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {file_path}'
                }
            
            if not full_path.is_file():
                return {
                    'success': False,
                    'error': f'Path is not a file: {file_path}'
                }
            
            # Read file content
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get file stats
            stats = full_path.stat()
            
            return {
                'success': True,
                'path': file_path,
                'name': full_path.name,
                'extension': full_path.suffix,
                'content': content,
                'size': len(content),
                'size_bytes': stats.st_size,
                'modified_time': stats.st_mtime
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'path': file_path
            }
    
    def _create_file_manifest(self, parsed_files: Dict, created_files: List, created_directories: List) -> Dict:
        """Create a manifest file with project metadata."""
        return {
            'project_id': self.project_id,
            'parsing_results': {
                'file_count': parsed_files.get('file_count', len(created_files)),
                'success': parsed_files.get('success', True),
                'parsing_errors': parsed_files.get('parsing_errors', [])
            },
            'project_structure': parsed_files.get('project_structure', {}),
            'created_files': created_files,
            'created_directories': created_directories,
            'file_types': self._analyze_file_types(created_files),
            'total_size': sum(f['size'] for f in created_files),
            'creation_timestamp': self._get_timestamp(),
            'template_metadata': parsed_files.get('metadata', {})
        }
    
    def _build_file_tree(self, path: Path, relative_to: Optional[Path] = None) -> Dict[str, Any]:
        """Build hierarchical file tree structure."""
        if relative_to is None:
            relative_to = path
        
        relative_path = path.relative_to(relative_to)
        
        if path.is_file():
            stats = path.stat()
            return {
                'name': path.name,
                'type': 'file',
                'path': str(relative_path),
                'extension': path.suffix,
                'size': stats.st_size,
                'modified_time': stats.st_mtime
            }
        else:
            children = []
            try:
                # Sort: directories first, then files, both alphabetically
                items = list(path.iterdir())
                items.sort(key=lambda x: (x.is_file(), x.name.lower()))
                
                for item in items:
                    children.append(self._build_file_tree(item, relative_to))
            except PermissionError:
                pass  # Skip directories we can't read
            
            return {
                'name': path.name if path != relative_to else f'project-{self.project_id}',
                'type': 'folder',
                'path': str(relative_path) if path != relative_to else '',
                'children': children
            }
    
    def _count_files_in_tree(self, tree: Dict) -> int:
        """Count total files in tree structure."""
        if tree['type'] == 'file':
            return 1
        
        count = 0
        for child in tree.get('children', []):
            count += self._count_files_in_tree(child)
        return count
    
    def _calculate_tree_size(self, tree: Dict) -> int:
        """Calculate total size of all files in tree."""
        if tree['type'] == 'file':
            return tree.get('size', 0)
        
        total_size = 0
        for child in tree.get('children', []):
            total_size += self._calculate_tree_size(child)
        return total_size
    
    def _analyze_file_types(self, created_files: List) -> Dict[str, int]:
        """Analyze file types and their counts."""
        type_counts = {}
        for file_info in created_files:
            ext = Path(file_info['path']).suffix or 'no_extension'
            type_counts[ext] = type_counts.get(ext, 0) + 1
        return type_counts
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as ISO string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def cleanup_project(self) -> Dict[str, Any]:
        """Clean up project files and directories."""
        try:
            if self.project_path.exists():
                shutil.rmtree(self.project_path)
                return {
                    'success': True,
                    'message': f'Project {self.project_id} cleaned up successfully'
                }
            else:
                return {
                    'success': True,
                    'message': f'Project {self.project_id} directory does not exist'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_project_info(self) -> Dict[str, Any]:
        """Get general project information."""
        try:
            manifest_path = self.project_path / "parsed_files.json"
            
            if manifest_path.exists():
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                return {
                    'success': True,
                    'manifest': manifest,
                    'has_files': self.files_path.exists(),
                    'has_zip': self.zip_path.exists(),
                    'zip_size': self.zip_path.stat().st_size if self.zip_path.exists() else 0
                }
            else:
                return {
                    'success': False,
                    'error': 'Project manifest not found'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def create_project_structure(project_id: str, parsed_files: Dict[str, Any], project_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to create complete project structure with template injection.
    
    Args:
        project_id: Unique project identifier
        parsed_files: Parsed files from CrewAI output
        project_metadata: Project metadata for template variables (optional)
    
    Returns:
        Dictionary with creation results
    """
    # Inject templates before creating project structure
    if project_metadata is None:
        # Extract basic metadata from parsed files if not provided
        project_metadata = {
            'title': f'Project {project_id}',
            'description': 'AI-generated website project'
        }
    
    # Inject template files
    enhanced_files = inject_templates(parsed_files, project_metadata)
    
    manager = ProjectStructureManager(project_id)
    
    # Create folder structure with enhanced files (including templates)
    folder_result = manager.create_project_folder(enhanced_files)
    if not folder_result['success']:
        return folder_result
    
    # Create ZIP archive
    zip_result = manager.create_zip_archive()
    
    return {
        'success': folder_result['success'] and zip_result['success'],
        'folder_result': folder_result,
        'zip_result': zip_result,
        'project_path': folder_result['project_path'],
        'zip_path': zip_result.get('zip_path'),
        'total_files': folder_result['total_files'],
        'zip_created': zip_result['success'],
        'templates_injected': folder_result.get('templates_injected', 0),
        'template_metadata': enhanced_files.get('metadata', {})
    }


def get_project_download_info(project_id: str) -> Dict[str, Any]:
    """Get download information for a project."""
    manager = ProjectStructureManager(project_id)
    return manager.get_project_info()
