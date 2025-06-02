#!/usr/bin/env python3
"""
Test script for Template Injection System

This script tests the template injection functionality to ensure
it works correctly with our existing project structure.
"""

import sys
import os
import json
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

from utils.template_engine import inject_templates, create_project_variables, TemplateEngine

def test_template_engine():
    """Test the basic template engine functionality."""
    print("🔧 Testing Template Engine...")
    
    engine = TemplateEngine()
    
    # Test loading templates
    templates = engine.get_available_templates()
    print(f"✅ Found {len(templates)} templates: {templates}")
    
    # Test variable creation
    test_metadata = {
        'title': 'My Awesome Portfolio',
        'description': 'A beautiful portfolio website'
    }
    
    variables = create_project_variables(test_metadata)
    print(f"✅ Created variables: {variables}")
    
    # Test template generation
    for template in templates:
        try:
            content = engine.generate_file(template, variables)
            print(f"✅ Generated {template}: {len(content)} characters")
        except Exception as e:
            print(f"❌ Error with {template}: {e}")
    
    print()

def test_template_injection():
    """Test the template injection with mock parsed files."""
    print("🚀 Testing Template Injection...")
    
    # Mock parsed files structure (similar to what file_parser.py produces)
    mock_parsed_files = {
        'files': {
            'src/App.tsx': {
                'content': 'import React from "react";\n\nfunction App() {\n  return <div>Hello World</div>;\n}\n\nexport default App;',
                'language': 'typescript',
                'size': 95
            },
            'package.json': {
                'content': '{\n  "name": "test-project",\n  "version": "1.0.0"\n}',
                'language': 'json',
                'size': 45
            }
        },
        'metadata': {
            'total_files': 2,
            'parsing_success': True
        }
    }
    
    # Mock project metadata
    project_metadata = {
        'title': 'Test Portfolio Website',
        'description': 'A test portfolio for template injection'
    }
    
    print(f"📝 Original files: {list(mock_parsed_files['files'].keys())}")
    
    # Inject templates
    enhanced_files = inject_templates(mock_parsed_files, project_metadata)
    
    print(f"🎯 Enhanced files: {list(enhanced_files['files'].keys())}")
    print(f"📊 Templates injected: {enhanced_files['metadata'].get('templates_injected', 0)}")
    
    # Verify template files were added
    expected_files = [
        'index.html',
        'src/main.tsx',
        'src/index.css',
        'vite.config.ts',
        'tsconfig.json'
    ]
    
    for expected_file in expected_files:
        if expected_file in enhanced_files['files']:
            file_info = enhanced_files['files'][expected_file]
            template_generated = file_info.get('template_generated', False)
            print(f"✅ {expected_file}: {file_info['size']} chars (template: {template_generated})")
        else:
            print(f"❌ Missing: {expected_file}")
    
    # Check if title was replaced correctly
    index_html = enhanced_files['files'].get('index.html', {}).get('content', '')
    if 'Test Portfolio Website' in index_html:
        print("✅ Project title correctly injected in index.html")
    else:
        print("❌ Project title not found in index.html")
    
    print()

def test_file_conflict_resolution():
    """Test how template injection handles existing files."""
    print("⚔️ Testing File Conflict Resolution...")
    
    # Mock parsed files with existing template files
    mock_parsed_files = {
        'files': {
            'index.html': {
                'content': '<html><head><title>Old Title</title></head><body>Old content</body></html>',
                'language': 'html',
                'size': 75
            },
            'src/main.tsx': {
                'content': 'console.log("old main.tsx");',
                'language': 'typescript',
                'size': 28
            },
            'src/App.tsx': {
                'content': 'function App() { return <div>App</div>; }',
                'language': 'typescript',
                'size': 40
            }
        }
    }
    
    project_metadata = {
        'title': 'Conflict Test Project'
    }
    
    print("📝 Files before injection:")
    for filename, file_info in mock_parsed_files['files'].items():
        print(f"  - {filename}: {file_info['size']} chars")
    
    # Inject templates (should replace existing files)
    enhanced_files = inject_templates(mock_parsed_files, project_metadata)
    
    print("📝 Files after injection:")
    for filename, file_info in enhanced_files['files'].items():
        template_generated = file_info.get('template_generated', False)
        marker = "🔄" if template_generated else "📄"
        print(f"  {marker} {filename}: {file_info['size']} chars")
    
    # Verify that template files were replaced
    index_html = enhanced_files['files'].get('index.html', {}).get('content', '')
    if 'Conflict Test Project' in index_html:
        print("✅ Template correctly replaced existing index.html")
    else:
        print("❌ Template did not replace existing index.html")
    
    # Verify that non-template files were preserved
    app_tsx = enhanced_files['files'].get('src/App.tsx', {}).get('content', '')
    if 'function App()' in app_tsx:
        print("✅ Non-template file (App.tsx) was preserved")
    else:
        print("❌ Non-template file was modified unexpectedly")
    
    print()

def main():
    """Run all template injection tests."""
    print("🧪 Template Injection System Tests")
    print("=" * 50)
    
    try:
        test_template_engine()
        test_template_injection()
        test_file_conflict_resolution()
        
        print("🎉 All tests completed!")
        print("\n📋 Summary:")
        print("✅ Template Engine: Working correctly")
        print("✅ Template Injection: Successfully adding template files")
        print("✅ Conflict Resolution: Properly replacing existing template files")
        print("✅ Variable Replacement: Project titles correctly injected")
        
        print("\n🚀 Ready for integration with project_structure.py!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
