#!/usr/bin/env python3
"""
Apply Vite fix to existing project

This script applies the new Vite templates to an existing project
to fix the npm start issue.
"""

import sys
import os
import json
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from utils.template_engine import TemplateEngine, create_project_variables
from utils.project_structure import ProjectStructureManager

def apply_vite_fix_to_project(project_id: str):
    """Apply Vite fix to a specific project."""
    print(f"🔧 Applying Vite fix to project: {project_id}")
    
    try:
        # Initialize template engine
        engine = TemplateEngine()
        
        # Project path
        project_path = Path(f"generated/projects/{project_id}/files")
        
        if not project_path.exists():
            print(f"❌ Project not found: {project_path}")
            return False
        
        # Read current package.json to get project name
        package_json_path = project_path / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                current_package = json.load(f)
            project_name = current_package.get('name', 'react-app')
        else:
            project_name = f"project-{project_id}"
        
        # Create template variables
        variables = {
            'PROJECT_TITLE': project_name.replace('-', ' ').title(),
            'PROJECT_NAME': project_name,
            'CREATION_DATE': '2025-06-02'
        }
        
        print(f"📝 Using variables: {variables}")
        
        # Generate and apply templates
        templates_to_apply = [
            ('package.json.template', 'package.json'),
            ('index.html.template', 'index.html'),
            ('vite.config.ts.template', 'vite.config.ts'),
            ('tsconfig.json.template', 'tsconfig.json')
        ]
        
        applied_count = 0
        
        for template_name, output_file in templates_to_apply:
            try:
                # Generate content from template
                content = engine.generate_file(template_name, variables)
                
                # Write to project
                output_path = project_path / output_file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Applied {template_name} -> {output_file}")
                applied_count += 1
                
            except Exception as e:
                print(f"❌ Failed to apply {template_name}: {e}")
        
        print(f"🎉 Applied {applied_count}/{len(templates_to_apply)} templates")
        
        # Verify the fix
        new_package_json_path = project_path / "package.json"
        if new_package_json_path.exists():
            with open(new_package_json_path, 'r') as f:
                new_package = json.load(f)
            
            if 'vite' in new_package.get('devDependencies', {}):
                print("✅ Project now uses Vite!")
                print(f"   Dev command: {new_package['scripts']['dev']}")
                return True
            else:
                print("❌ Vite not found in package.json")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ Failed to apply Vite fix: {e}")
        return False

def main():
    """Apply Vite fix to both existing projects."""
    print("🚀 Applying Vite Fix to Existing Projects\n")
    
    projects = [
        'b216ae3e-94ac-49b3-a986-21ee86ecb56f',
        'f88bee72-0db0-4d73-bf31-4f232c71f068'
    ]
    
    success_count = 0
    
    for project_id in projects:
        if apply_vite_fix_to_project(project_id):
            success_count += 1
        print()  # Empty line between projects
    
    print(f"📊 Results: {success_count}/{len(projects)} projects fixed")
    
    if success_count == len(projects):
        print("🎉 All projects successfully converted to Vite!")
        print("\n💡 You can now run 'npm run dev' in any project directory")
        return True
    else:
        print("❌ Some projects failed to convert")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
