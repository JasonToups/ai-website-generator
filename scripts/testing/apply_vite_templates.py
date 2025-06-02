#!/usr/bin/env python3
"""
Apply updated Vite templates to existing project

This script applies the new Vite templates to fix the shopping list app
and make it work with proper Vite development setup.
"""

import sys
import os
import json
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from utils.template_engine import TemplateEngine, create_project_variables
from utils.project_structure import ProjectStructureManager

def apply_vite_templates_to_project(project_id: str):
    """Apply Vite templates to a specific project."""
    print(f"🔧 Applying Vite templates to project: {project_id}")
    
    try:
        # Initialize template engine
        engine = TemplateEngine()
        
        # Project path
        project_path = Path(f"generated/projects/{project_id}/files")
        
        if not project_path.exists():
            print(f"❌ Project not found: {project_path}")
            return False
        
        # Create project metadata for template variables
        project_metadata = {
            'title': 'Shopping List App',  # We'll extract this from the actual project later
            'description': 'AI-generated shopping list application'
        }
        
        # Create template variables
        variables = create_project_variables(project_metadata)
        print(f"📝 Using variables: {variables}")
        
        # Get all available templates
        available_templates = engine.get_available_templates()
        print(f"📋 Available templates: {available_templates}")
        
        # Template mappings
        template_mappings = {
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
        
        applied_count = 0
        
        for template_name, output_file in template_mappings.items():
            if template_name in available_templates:
                try:
                    # Generate content from template
                    content = engine.generate_file(template_name, variables)
                    
                    # Write to project
                    output_path = project_path / output_file
                    
                    # Create directory if needed
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ Applied {template_name} -> {output_file}")
                    applied_count += 1
                    
                except Exception as e:
                    print(f"❌ Failed to apply {template_name}: {e}")
            else:
                print(f"⚠️  Template not found: {template_name}")
        
        print(f"🎉 Applied {applied_count}/{len(template_mappings)} templates")
        
        # Verify the result
        package_json_path = project_path / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            if 'vite' in package_data.get('devDependencies', {}):
                print("✅ Project now uses Vite!")
                print(f"   Dev command: {package_data['scripts']['dev']}")
                
                # Check for React Router
                if 'react-router-dom' in package_data.get('dependencies', {}):
                    print("✅ React Router included!")
                
                return True
            else:
                print("❌ Vite not found in package.json")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ Failed to apply Vite templates: {e}")
        return False

def main():
    """Apply Vite templates to the shopping list project."""
    print("🚀 Applying Vite Templates to Shopping List Project\n")
    
    project_id = '9ab87061-070a-43b2-b967-b58d734706ad'
    
    if apply_vite_templates_to_project(project_id):
        print("\n🎉 Success! The shopping list app now has proper Vite setup.")
        print(f"📁 Project location: generated/projects/{project_id}/files")
        print("💡 You can now run 'npm install && npm run dev' in the project directory")
        return True
    else:
        print("\n❌ Failed to apply Vite templates")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
