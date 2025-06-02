"""File parser module for extracting individual files from crew output text."""

import re
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class ProjectFileParser:
    """Parse crew output text into individual project files."""
    
    def __init__(self, crew_output: str, project_id: str):
        self.crew_output = crew_output
        self.project_id = project_id
        self.files = {}
        self.project_structure = {}
        self.parsing_errors = []
    
    def parse(self) -> Dict[str, Any]:
        """Main parsing method that extracts all files from crew output."""
        try:
            # 1. Extract file blocks from the text
            file_blocks = self.extract_file_blocks()
            
            # 2. Parse each file block
            for block in file_blocks:
                parsed_file = self.parse_file_content(block)
                if parsed_file:
                    self.files[parsed_file['path']] = parsed_file
            
            # 3. Create project structure
            self.project_structure = self.create_project_structure()
            
            # 4. Validate all extracted content
            self.validate_all_files()
            
            return {
                'files': self.files,
                'project_structure': self.project_structure,
                'file_count': len(self.files),
                'parsing_errors': self.parsing_errors,
                'success': len(self.parsing_errors) == 0
            }
            
        except Exception as e:
            self.parsing_errors.append(f"Critical parsing error: {str(e)}")
            return {
                'files': {},
                'project_structure': {},
                'file_count': 0,
                'parsing_errors': self.parsing_errors,
                'success': False
            }
    
    def extract_file_blocks(self) -> List[Dict]:
        """Extract file blocks from crew output text."""
        file_blocks = []
        
        # Try multiple patterns to handle different crew output formats
        patterns = [
            # Pattern 1: Numbered files (legacy format)
            r'(\d+)\.\s+([^\n]+)\n\n```(\w+)\n(.*?)\n```',
            # Pattern 2: File path with colon (new format)
            r'([^\n]+\.[a-zA-Z]+):\n\n```(\w+)\n(.*?)\n```'
        ]
        
        for pattern_idx, pattern in enumerate(patterns):
            matches = re.findall(pattern, self.crew_output, re.DOTALL)
            
            if matches:
                print(f"Using pattern {pattern_idx + 1}: found {len(matches)} matches")
                
                for match_idx, match in enumerate(matches):
                    if pattern_idx == 0:  # Numbered format
                        file_number, file_path, language, content = match
                        file_blocks.append({
                            'number': int(file_number),
                            'path': file_path.strip(),
                            'language': language.strip(),
                            'content': content.strip(),
                            'raw_match': match
                        })
                    else:  # Colon format
                        file_path, language, content = match
                        file_blocks.append({
                            'number': match_idx + 1,  # Assign sequential numbers
                            'path': file_path.strip(),
                            'language': language.strip(),
                            'content': content.strip(),
                            'raw_match': match
                        })
                
                # Sort by file number to maintain order
                file_blocks.sort(key=lambda x: x['number'])
                break  # Use first pattern that finds matches
        
        return file_blocks
    
    def parse_file_content(self, file_block: Dict) -> Optional[Dict]:
        """Parse individual file content and metadata."""
        try:
            file_path = file_block['path']
            content = file_block['content']
            language = file_block['language']
            
            # Extract file extension and name
            path_obj = Path(file_path)
            file_name = path_obj.name
            file_extension = path_obj.suffix
            directory = str(path_obj.parent) if path_obj.parent != Path('.') else ''
            
            # Validate content based on file type
            is_valid, validation_error = self.validate_content(content, file_extension)
            
            if not is_valid:
                self.parsing_errors.append(f"Validation failed for {file_path}: {validation_error}")
            
            return {
                'path': file_path,
                'name': file_name,
                'extension': file_extension,
                'directory': directory,
                'content': content,
                'language': language,
                'size': len(content),
                'is_valid': is_valid,
                'validation_error': validation_error if not is_valid else None,
                'file_number': file_block['number']
            }
            
        except Exception as e:
            error_msg = f"Error parsing file block {file_block.get('number', 'unknown')}: {str(e)}"
            self.parsing_errors.append(error_msg)
            return None
    
    def validate_content(self, content: str, file_extension: str) -> Tuple[bool, Optional[str]]:
        """Validate file content based on file type."""
        try:
            if file_extension in ['.tsx', '.ts', '.jsx', '.js']:
                return self.validate_typescript_content(content)
            elif file_extension == '.json':
                return self.validate_json_content(content)
            elif file_extension == '.md':
                return self.validate_markdown_content(content)
            elif file_extension in ['.css', '.scss']:
                return self.validate_css_content(content)
            else:
                # For other file types, just check if content is not empty
                return len(content.strip()) > 0, None if len(content.strip()) > 0 else "Empty file content"
                
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def validate_typescript_content(self, content: str) -> Tuple[bool, Optional[str]]:
        """Validate TypeScript/JavaScript content."""
        # Basic validation checks
        checks = [
            # Check for basic syntax elements
            ('import' in content or 'export' in content or 'function' in content or 'const' in content, 
             "No import/export/function/const statements found"),
            
            # Check for balanced braces (basic check)
            (content.count('{') == content.count('}'), "Unbalanced curly braces"),
            
            # Check for balanced parentheses
            (content.count('(') == content.count(')'), "Unbalanced parentheses"),
            
            # Check for React component patterns if it's a .tsx file
            (True, None)  # Always pass for now, can add more specific React checks
        ]
        
        for is_valid, error_msg in checks:
            if not is_valid:
                return False, error_msg
        
        return True, None
    
    def validate_json_content(self, content: str) -> Tuple[bool, Optional[str]]:
        """Validate JSON content."""
        try:
            json.loads(content)
            return True, None
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
    
    def validate_markdown_content(self, content: str) -> Tuple[bool, Optional[str]]:
        """Validate Markdown content."""
        # Basic markdown validation
        if len(content.strip()) == 0:
            return False, "Empty markdown content"
        
        # Check for basic markdown elements
        has_content = any([
            '#' in content,  # Headers
            '*' in content,  # Lists or emphasis
            '`' in content,  # Code blocks
            len(content.split('\n')) > 1  # Multiple lines
        ])
        
        return has_content, None if has_content else "No markdown formatting detected"
    
    def validate_css_content(self, content: str) -> Tuple[bool, Optional[str]]:
        """Validate CSS content."""
        # Basic CSS validation
        if len(content.strip()) == 0:
            return False, "Empty CSS content"
        
        # Check for basic CSS syntax
        has_css_syntax = any([
            '{' in content and '}' in content,  # CSS rules
            ':' in content,  # Properties
            ';' in content   # Property endings
        ])
        
        return has_css_syntax, None if has_css_syntax else "No CSS syntax detected"
    
    def create_project_structure(self) -> Dict[str, Any]:
        """Create hierarchical project structure from parsed files."""
        structure = {
            'name': f'project-{self.project_id}',
            'type': 'folder',
            'children': {}
        }
        
        for file_path, file_info in self.files.items():
            self._add_file_to_structure(structure, file_path, file_info)
        
        # Convert children dict to list for easier frontend consumption
        structure['children'] = self._convert_structure_to_list(structure['children'])
        
        return structure
    
    def _add_file_to_structure(self, structure: Dict, file_path: str, file_info: Dict):
        """Add a file to the hierarchical structure."""
        path_parts = file_path.split('/')
        current = structure['children']
        
        # Navigate/create directory structure
        for i, part in enumerate(path_parts[:-1]):
            if part not in current:
                current[part] = {
                    'name': part,
                    'type': 'folder',
                    'children': {}
                }
            current = current[part]['children']
        
        # Add the file
        file_name = path_parts[-1]
        current[file_name] = {
            'name': file_name,
            'type': 'file',
            'path': file_path,
            'extension': file_info['extension'],
            'size': file_info['size'],
            'is_valid': file_info['is_valid']
        }
    
    def _convert_structure_to_list(self, children_dict: Dict) -> List[Dict]:
        """Convert children dictionary to list format."""
        children_list = []
        
        # Sort: folders first, then files, both alphabetically
        items = list(children_dict.items())
        items.sort(key=lambda x: (x[1]['type'] == 'file', x[0].lower()))
        
        for name, item in items:
            if item['type'] == 'folder':
                item['children'] = self._convert_structure_to_list(item['children'])
            children_list.append(item)
        
        return children_list
    
    def validate_all_files(self):
        """Run additional validation on all parsed files."""
        # Check for required files
        required_files = ['package.json', 'README.md']
        found_required = []
        
        for file_path in self.files.keys():
            file_name = Path(file_path).name
            if file_name in required_files:
                found_required.append(file_name)
        
        missing_required = set(required_files) - set(found_required)
        if missing_required:
            self.parsing_errors.append(f"Missing required files: {', '.join(missing_required)}")
        
        # Check for React app structure
        has_app_tsx = any('App.tsx' in path for path in self.files.keys())
        has_components = any('components/' in path for path in self.files.keys())
        
        if not has_app_tsx:
            self.parsing_errors.append("No App.tsx file found")
        
        if not has_components:
            self.parsing_errors.append("No components directory found")
    
    def get_parsing_summary(self) -> Dict[str, Any]:
        """Get a summary of the parsing results."""
        return {
            'total_files': len(self.files),
            'valid_files': sum(1 for f in self.files.values() if f['is_valid']),
            'invalid_files': sum(1 for f in self.files.values() if not f['is_valid']),
            'file_types': self._get_file_type_counts(),
            'parsing_errors': len(self.parsing_errors),
            'success_rate': (sum(1 for f in self.files.values() if f['is_valid']) / len(self.files) * 100) if self.files else 0
        }
    
    def _get_file_type_counts(self) -> Dict[str, int]:
        """Get count of files by extension."""
        type_counts = {}
        for file_info in self.files.values():
            ext = file_info['extension'] or 'no_extension'
            type_counts[ext] = type_counts.get(ext, 0) + 1
        return type_counts


def parse_project_files(crew_output: str, project_id: str) -> Dict[str, Any]:
    """Convenience function to parse project files from crew output."""
    parser = ProjectFileParser(crew_output, project_id)
    return parser.parse()


def get_parsing_summary(crew_output: str, project_id: str) -> Dict[str, Any]:
    """Get a summary of parsing results without full parsing."""
    parser = ProjectFileParser(crew_output, project_id)
    parser.extract_file_blocks()
    return parser.get_parsing_summary()
