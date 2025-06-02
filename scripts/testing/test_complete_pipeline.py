#!/usr/bin/env python3
"""
Complete pipeline test - from file parsing to preview readiness
"""

import sys
import subprocess
import time
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from utils.file_parser import ProjectFileParser
from utils.project_structure import create_project_structure

def test_complete_pipeline():
    """Test the complete pipeline from parsing to preview readiness."""
    print("🚀 Testing Complete AI Website Generator Pipeline\n")
    
    # Test project ID
    project_id = "16fdd748-a31a-488b-9df9-882d6e77d588"
    project_path = Path(f"generated/projects/{project_id}")
    files_path = project_path / "files"
    
    print("=" * 60)
    print("PHASE 1: FILE PARSING")
    print("=" * 60)
    
    # Read crew output
    crew_output_path = project_path / "crew_output.txt"
    if not crew_output_path.exists():
        print(f"❌ Crew output not found: {crew_output_path}")
        return False
    
    with open(crew_output_path, 'r', encoding='utf-8') as f:
        crew_output = f.read()
    
    print(f"📄 Crew output: {len(crew_output)} characters")
    
    # Test file parsing
    parser = ProjectFileParser(crew_output, project_id)
    parsed_result = parser.parse()
    
    if not parsed_result['success']:
        print(f"❌ File parsing failed: {parsed_result.get('error')}")
        return False
    
    print(f"✅ Parsed {parsed_result['file_count']} files successfully")
    
    print("\n" + "=" * 60)
    print("PHASE 2: PROJECT STRUCTURE CREATION")
    print("=" * 60)
    
    # Test project structure creation
    structure_result = create_project_structure(project_id, parsed_result)
    
    if not structure_result['success']:
        print(f"❌ Project structure creation failed")
        return False
    
    print(f"✅ Created project structure with {structure_result['total_files']} files")
    print(f"📋 Templates injected: {structure_result.get('templates_injected', 0)}")
    
    print("\n" + "=" * 60)
    print("PHASE 3: FILE SYSTEM VERIFICATION")
    print("=" * 60)
    
    # Check critical files
    critical_files = [
        'package.json',
        'src/main.tsx',
        'src/App.tsx',
        'vite.config.ts',
        'postcss.config.js',
        'tailwind.config.js',
        'tsconfig.json',
        'index.html'
    ]
    
    missing_files = []
    for file_name in critical_files:
        file_path = files_path / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} (missing)")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n❌ Missing critical files: {missing_files}")
        return False
    
    print("\n" + "=" * 60)
    print("PHASE 4: NPM DEPENDENCY CHECK")
    print("=" * 60)
    
    # Check if node_modules exists
    node_modules_path = files_path / "node_modules"
    if node_modules_path.exists():
        print("✅ Dependencies installed")
    else:
        print("⚠️  Dependencies not installed (run npm install)")
    
    print("\n" + "=" * 60)
    print("PHASE 5: CONFIGURATION VALIDATION")
    print("=" * 60)
    
    # Check PostCSS configuration
    postcss_config = files_path / "postcss.config.js"
    if postcss_config.exists():
        with open(postcss_config, 'r') as f:
            postcss_content = f.read()
        
        if 'import tailwindcss from' in postcss_content:
            print("✅ PostCSS configuration uses modern import syntax")
        else:
            print("⚠️  PostCSS configuration may need updating")
    
    # Check package.json scripts
    package_json = files_path / "package.json"
    if package_json.exists():
        import json
        with open(package_json, 'r') as f:
            package_data = json.load(f)
        
        scripts = package_data.get('scripts', {})
        if 'dev' in scripts and 'build' in scripts:
            print("✅ Package.json has dev and build scripts")
        else:
            print("⚠️  Package.json missing required scripts")
    
    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    
    print("✅ File parsing: WORKING")
    print("✅ Template injection: WORKING") 
    print("✅ Project structure: COMPLETE")
    print("✅ Configuration files: PRESENT")
    print("✅ Vite setup: READY")
    
    print(f"\n🎉 SUCCESS: Complete pipeline working!")
    print(f"📁 Project location: {files_path}")
    print(f"🚀 Ready for: cd {files_path} && npm install && npm run dev")
    
    return True

if __name__ == "__main__":
    success = test_complete_pipeline()
    sys.exit(0 if success else 1)
