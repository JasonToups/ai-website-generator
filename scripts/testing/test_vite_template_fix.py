#!/usr/bin/env python3
"""
Test script for Vite template fix

This script tests the new package.json template and verifies that
it correctly overrides CrewAI-generated package.json files.
"""

import sys
import os
import json
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from utils.template_engine import TemplateEngine, inject_templates, create_project_variables

def test_package_json_template():
    """Test the new package.json template."""
    print("🧪 Testing package.json template...")
    
    try:
        # Initialize template engine
        engine = TemplateEngine()
        
        # Test variables
        test_variables = {
            'PROJECT_TITLE': 'Photographer Portfolio',
            'PROJECT_NAME': 'photographer-portfolio',
            'CREATION_DATE': '2025-06-02'
        }
        
        # Generate package.json from template
        package_json_content = engine.generate_file('package.json.template', test_variables)
        
        # Parse the generated JSON to verify it's valid
        package_data = json.loads(package_json_content)
        
        print(f"✅ Template generated successfully")
        print(f"   Project name: {package_data['name']}")
        print(f"   Type: {package_data['type']}")
        print(f"   Scripts: {list(package_data['scripts'].keys())}")
        print(f"   Dependencies: {list(package_data['dependencies'].keys())}")
        print(f"   DevDependencies: {list(package_data['devDependencies'].keys())}")
        
        # Verify it's a Vite project
        assert 'vite' in package_data['devDependencies'], "Vite not found in devDependencies"
        assert '@vitejs/plugin-react' in package_data['devDependencies'], "Vite React plugin not found"
        assert package_data['scripts']['dev'] == 'vite', "Dev script should use Vite"
        assert package_data['type'] == 'module', "Should be ES module type"
        
        print("✅ All Vite-specific checks passed")
        return True
        
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        return False

def test_template_injection():
    """Test template injection with mock CrewAI output."""
    print("\n🧪 Testing template injection...")
    
    try:
        # Mock CrewAI output with CRA-style package.json
        mock_parsed_files = {
            'files': {
                'package.json': {
                    'content': json.dumps({
                        "name": "photographer-portfolio",
                        "version": "0.1.0",
                        "private": True,
                        "dependencies": {
                            "react": "^18.2.0",
                            "react-dom": "^18.2.0",
                            "react-scripts": "5.0.1"
                        },
                        "scripts": {
                            "start": "react-scripts start",
                            "build": "react-scripts build"
                        }
                    }, indent=2),
                    'language': 'json',
                    'size': 200
                },
                'src/App.tsx': {
                    'content': 'import React from "react";\n\nfunction App() {\n  return <div>Hello</div>;\n}\n\nexport default App;',
                    'language': 'typescript',
                    'size': 100
                }
            },
            'file_count': 2,
            'success': True
        }
        
        # Mock project metadata
        project_metadata = {
            'title': 'Photographer Portfolio',
            'description': 'A beautiful portfolio website'
        }
        
        # Inject templates
        enhanced_files = inject_templates(mock_parsed_files, project_metadata)
        
        # Verify package.json was replaced
        package_json_content = enhanced_files['files']['package.json']['content']
        package_data = json.loads(package_json_content)
        
        print(f"✅ Template injection successful")
        print(f"   Templates injected: {enhanced_files['metadata']['templates_injected']}")
        print(f"   Package.json now uses: {package_data['scripts']['dev']}")
        
        # Verify it's now a Vite project
        assert 'vite' in package_data['devDependencies'], "Package.json should now have Vite"
        assert package_data['scripts']['dev'] == 'vite', "Dev script should now use Vite"
        assert 'react-scripts' not in package_data.get('dependencies', {}), "Should not have react-scripts"
        
        # Verify other templates were injected
        assert 'vite.config.ts' in enhanced_files['files'], "vite.config.ts should be injected"
        assert 'tsconfig.json' in enhanced_files['files'], "tsconfig.json should be injected"
        
        print("✅ All injection checks passed")
        return True
        
    except Exception as e:
        print(f"❌ Template injection test failed: {e}")
        return False

def test_available_templates():
    """Test that all expected templates are available."""
    print("\n🧪 Testing available templates...")
    
    try:
        engine = TemplateEngine()
        templates = engine.get_available_templates()
        
        expected_templates = [
            'package.json.template',
            'index.html.template',
            'main.tsx.template',
            'index.css.template',
            'vite.config.ts.template',
            'tsconfig.json.template'
        ]
        
        print(f"✅ Found templates: {templates}")
        
        for template in expected_templates:
            assert template in templates, f"Missing template: {template}"
        
        print("✅ All expected templates found")
        return True
        
    except Exception as e:
        print(f"❌ Template availability test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Vite Template Fix\n")
    
    tests = [
        test_available_templates,
        test_package_json_template,
        test_template_injection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Template system is ready.")
        return True
    else:
        print("❌ Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
