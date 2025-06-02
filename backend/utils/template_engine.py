"""
Template Engine for AI Website Generator

This module handles loading template files and replacing dynamic variables
to generate project-specific boilerplate files.
"""

import os
import re
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TemplateEngine:
    """
    Template engine for processing project template files.
    
    Handles loading template files from backend/templates/ directory
    and replacing dynamic variables with project-specific values.
    """
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the template engine.
        
        Args:
            templates_dir: Path to templates directory. Defaults to backend/templates/
        """
        if templates_dir is None:
            # Get the directory where this file is located
            current_dir = Path(__file__).parent
            # Go up to backend/ then into templates/
            self.templates_dir = current_dir.parent / "templates"
        else:
            self.templates_dir = Path(templates_dir)
        
        logger.info(f"Template engine initialized with directory: {self.templates_dir}")
    
    def load_template(self, template_name: str) -> str:
        """
        Load a template file from the templates directory.
        
        Args:
            template_name: Name of the template file (e.g., 'index.html.template')
        
        Returns:
            Template content as string
        
        Raises:
            FileNotFoundError: If template file doesn't exist
            IOError: If template file can't be read
        """
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.debug(f"Loaded template: {template_name} ({len(content)} characters)")
            return content
        
        except Exception as e:
            logger.error(f"Error loading template {template_name}: {e}")
            raise IOError(f"Failed to read template file: {template_path}") from e
    
    def replace_variables(self, template_content: str, variables: Dict[str, Any]) -> str:
        """
        Replace template variables with actual values.
        
        Variables are in the format {{VARIABLE_NAME}} and are replaced with
        corresponding values from the variables dictionary.
        
        Args:
            template_content: Template content with variables
            variables: Dictionary of variable names to values
        
        Returns:
            Template content with variables replaced
        """
        result = template_content
        
        # Find all variables in the template (format: {{VARIABLE_NAME}})
        variable_pattern = r'\{\{([A-Z_]+)\}\}'
        found_variables = re.findall(variable_pattern, result)
        
        logger.debug(f"Found variables in template: {found_variables}")
        
        # Replace each variable with its value
        for var_name in found_variables:
            if var_name in variables:
                placeholder = f"{{{{{var_name}}}}}"
                value = str(variables[var_name])
                result = result.replace(placeholder, value)
                logger.debug(f"Replaced {placeholder} with '{value}'")
            else:
                logger.warning(f"Variable {var_name} not found in variables dictionary")
        
        return result
    
    def generate_file(self, template_name: str, variables: Dict[str, Any]) -> str:
        """
        Generate a file from a template with variable replacement.
        
        Args:
            template_name: Name of the template file
            variables: Dictionary of variables to replace
        
        Returns:
            Generated file content
        """
        template_content = self.load_template(template_name)
        return self.replace_variables(template_content, variables)
    
    def get_available_templates(self) -> list[str]:
        """
        Get list of available template files.
        
        Returns:
            List of template file names
        """
        if not self.templates_dir.exists():
            return []
        
        templates = []
        for file_path in self.templates_dir.glob("*.template"):
            templates.append(file_path.name)
        
        return sorted(templates)
    
    def validate_template(self, template_name: str) -> Dict[str, Any]:
        """
        Validate a template file and return information about it.
        
        Args:
            template_name: Name of the template file
        
        Returns:
            Dictionary with validation results:
            - valid: bool - Whether template is valid
            - variables: list - Variables found in template
            - errors: list - Any validation errors
        """
        result = {
            'valid': True,
            'variables': [],
            'errors': []
        }
        
        try:
            content = self.load_template(template_name)
            
            # Find all variables
            variable_pattern = r'\{\{([A-Z_]+)\}\}'
            variables = re.findall(variable_pattern, content)
            result['variables'] = list(set(variables))  # Remove duplicates
            
            # Basic validation checks
            if not content.strip():
                result['valid'] = False
                result['errors'].append("Template is empty")
            
            # Check for malformed variables
            malformed_pattern = r'\{[^{]|\}[^}]|\{\{\w*[^A-Z_\w]\w*\}\}'
            if re.search(malformed_pattern, content):
                result['valid'] = False
                result['errors'].append("Template contains malformed variables")
            
        except Exception as e:
            result['valid'] = False
            result['errors'].append(str(e))
        
        return result


def create_project_variables(project_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create template variables from project metadata.
    
    Args:
        project_metadata: Project information dictionary
    
    Returns:
        Dictionary of template variables
    """
    import re
    from datetime import datetime
    
    # Extract project title from metadata
    project_title = project_metadata.get('title', 'React Application')
    
    # Generate project name (sanitized for technical use)
    project_name = re.sub(r'[^a-zA-Z0-9\-]', '-', project_title.lower())
    project_name = re.sub(r'-+', '-', project_name).strip('-')
    
    # Get creation date
    creation_date = datetime.now().strftime('%Y-%m-%d')
    
    variables = {
        'PROJECT_TITLE': project_title,
        'PROJECT_NAME': project_name,
        'CREATION_DATE': creation_date
    }
    
    logger.info(f"Created template variables: {variables}")
    return variables


# Template file mappings (template name -> output file path)
TEMPLATE_MAPPINGS = {
    'package.json.template': 'package.json',
    'index.html.template': 'index.html',
    'main.tsx.template': 'src/main.tsx',
    'index.css.template': 'src/index.css',
    'vite.config.ts.template': 'vite.config.ts',
    'tsconfig.json.template': 'tsconfig.json',
    'tsconfig.node.json.template': 'tsconfig.node.json',
    'tailwind.config.js.template': 'tailwind.config.js',
    'postcss.config.js.template': 'postcss.config.js'
}


def inject_templates(parsed_files: Dict[str, Any], project_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inject template files into parsed project structure.
    
    This is the main function that integrates with the project structure creation.
    
    Args:
        parsed_files: Parsed files from CrewAI output
        project_metadata: Project information for template variables
    
    Returns:
        Enhanced parsed_files with template files added
    """
    logger.info("Starting template injection process")
    
    try:
        # Initialize template engine
        engine = TemplateEngine()
        
        # Create template variables
        variables = create_project_variables(project_metadata)
        
        # Get available templates
        available_templates = engine.get_available_templates()
        logger.info(f"Available templates: {available_templates}")
        
        # Inject each template
        injected_count = 0
        for template_name in available_templates:
            if template_name in TEMPLATE_MAPPINGS:
                output_path = TEMPLATE_MAPPINGS[template_name]
                
                # Check if file already exists in parsed files
                if output_path in parsed_files.get('files', {}):
                    logger.info(f"File {output_path} already exists, replacing with template")
                
                # Generate file content from template
                try:
                    file_content = engine.generate_file(template_name, variables)
                    
                    # Add to parsed files structure
                    if 'files' not in parsed_files:
                        parsed_files['files'] = {}
                    
                    parsed_files['files'][output_path] = {
                        'content': file_content,
                        'language': _get_file_language(output_path),
                        'size': len(file_content),
                        'template_generated': True,
                        'template_source': template_name
                    }
                    
                    injected_count += 1
                    logger.info(f"Injected template: {template_name} -> {output_path}")
                
                except Exception as e:
                    logger.error(f"Failed to inject template {template_name}: {e}")
        
        # Update metadata
        if 'metadata' not in parsed_files:
            parsed_files['metadata'] = {}
        
        parsed_files['metadata']['templates_injected'] = injected_count
        parsed_files['metadata']['template_variables'] = variables
        
        logger.info(f"Template injection complete. Injected {injected_count} templates")
        return parsed_files
    
    except Exception as e:
        logger.error(f"Template injection failed: {e}")
        # Return original parsed_files if injection fails
        return parsed_files


def _get_file_language(file_path: str) -> str:
    """
    Determine file language from file extension.
    
    Args:
        file_path: Path to the file
    
    Returns:
        Language identifier
    """
    extension = Path(file_path).suffix.lower()
    
    language_map = {
        '.html': 'html',
        '.tsx': 'typescript',
        '.ts': 'typescript',
        '.css': 'css',
        '.json': 'json',
        '.js': 'javascript',
        '.jsx': 'javascript'
    }
    
    return language_map.get(extension, 'text')


if __name__ == "__main__":
    # Test the template engine
    logging.basicConfig(level=logging.DEBUG)
    
    engine = TemplateEngine()
    
    # Test loading templates
    templates = engine.get_available_templates()
    print(f"Available templates: {templates}")
    
    # Test variable replacement
    test_variables = {
        'PROJECT_TITLE': 'My Test Project',
        'PROJECT_NAME': 'my-test-project',
        'CREATION_DATE': '2025-05-29'
    }
    
    for template in templates:
        try:
            content = engine.generate_file(template, test_variables)
            print(f"\n--- {template} ---")
            print(content[:200] + "..." if len(content) > 200 else content)
        except Exception as e:
            print(f"Error with {template}: {e}")
