#!/usr/bin/env python3
"""
Final test to verify the Vite solution is working

This script verifies that:
1. Both projects have been converted to Vite
2. Template system is working for new projects
3. All files are in the correct structure
"""

import sys
import os
import json
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from utils.template_engine import TemplateEngine, inject_templates

def verify_project_structure(project_id: str):
    """Verify a project has the correct Vite structure."""
    print(f"🔍 Verifying project: {project_id}")
    
    project_path = Path(f"generated/projects/{project_id}/files")
    
    if not project_path.exists():
        print(f"❌ Project not found: {project_path}")
        return False
    
    # Check required files
    required_files = [
        'package.json',
        'vite.config.ts',
        'tsconfig.json',
        'index.html',
        'src/main.tsx',
        'src/App.tsx'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (project_path / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    # Check package.json is Vite-based
    package_json_path = project_path / "package.json"
    with open(package_json_path, 'r') as f:
        package_data = json.load(f)
    
    # Verify Vite setup
    checks = [
        ('type', 'module'),
        ('scripts.dev', 'vite'),
        ('devDependencies.vite', True),
        ('devDependencies.@vitejs/plugin-react', True)
    ]
    
    for check_path, expected in checks:
        keys = check_path.split('.')
        value = package_data
        
        try:
            if expected is True:
                # For dependency checks, navigate to parent and check if final key exists
                for key in keys[:-1]:
                    value = value[key]
                if keys[-1] not in value:
                    print(f"❌ Missing dependency: {check_path}")
                    return False
            else:
                # For value checks, navigate to the actual value
                for key in keys:
                    value = value[key]
                if value != expected:
                    print(f"❌ Incorrect value for {check_path}: {value} (expected {expected})")
                    return False
        except (KeyError, TypeError):
            print(f"❌ Missing or invalid: {check_path}")
            return False
    
    print(f"✅ Project structure verified")
    return True

def test_template_system():
    """Test that the template system works correctly."""
    print("\n🧪 Testing template system...")
    
    try:
        # Mock project data
        mock_parsed_files = {
            'files': {
                'src/App.tsx': {
                    'content': 'import React from "react";\n\nfunction App() {\n  return <div>Hello</div>;\n}\n\nexport default App;',
                    'language': 'typescript',
                    'size': 100
                }
            },
            'file_count': 1,
            'success': True
        }
        
        project_metadata = {
            'title': 'Test Project',
            'description': 'A test project'
        }
        
        # Inject templates
        enhanced_files = inject_templates(mock_parsed_files, project_metadata)
        
        # Verify all templates were injected
        expected_files = [
            'package.json',
            'index.html',
            'src/main.tsx',
            'src/index.css',
            'vite.config.ts',
            'tsconfig.json'
        ]
        
        for file_path in expected_files:
            if file_path not in enhanced_files['files']:
                print(f"❌ Template not injected: {file_path}")
                return False
        
        # Verify package.json is Vite-based
        package_json_content = enhanced_files['files']['package.json']['content']
        package_data = json.loads(package_json_content)
        
        if package_data['scripts']['dev'] != 'vite':
            print(f"❌ Package.json not using Vite")
            return False
        
        print(f"✅ Template system working correctly")
        print(f"   Templates injected: {enhanced_files['metadata']['templates_injected']}")
        return True
        
    except Exception as e:
        print(f"❌ Template system test failed: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🚀 Final Vite Solution Verification\n")
    
    # Test existing projects
    projects = [
        'b216ae3e-94ac-49b3-a986-21ee86ecb56f',
        'f88bee72-0db0-4d73-bf31-4f232c71f068'
    ]
    
    project_success = 0
    for project_id in projects:
        if verify_project_structure(project_id):
            project_success += 1
        print()
    
    # Test template system
    template_success = test_template_system()
    
    print(f"\n📊 Final Results:")
    print(f"   Existing projects converted: {project_success}/{len(projects)}")
    print(f"   Template system working: {'✅' if template_success else '❌'}")
    
    if project_success == len(projects) and template_success:
        print("\n🎉 SUCCESS: Vite solution is fully working!")
        print("\n💡 Summary:")
        print("   • Both existing projects converted to Vite")
        print("   • Template system will generate Vite projects")
        print("   • Users can now run 'npm run dev' instead of 'npm start'")
        print("   • Preview system continues to work unchanged")
        return True
    else:
        print("\n❌ Some issues remain. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
