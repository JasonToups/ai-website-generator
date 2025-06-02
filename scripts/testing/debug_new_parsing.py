#!/usr/bin/env python3
"""
Debug script to test file parsing on the new Vite-native crew output
"""

import sys
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from utils.file_parser import ProjectFileParser
from utils.project_structure import create_project_structure

def test_parsing():
    """Test parsing the new crew output."""
    print("🔍 Testing File Parsing on New Crew Output\n")
    
    # Read the crew output
    project_id = "16fdd748-a31a-488b-9df9-882d6e77d588"
    crew_output_path = Path(f"generated/projects/{project_id}/crew_output.txt")
    
    if not crew_output_path.exists():
        print(f"❌ Crew output file not found: {crew_output_path}")
        return False
    
    with open(crew_output_path, 'r', encoding='utf-8') as f:
        crew_output = f.read()
    
    print(f"📄 Crew output length: {len(crew_output)} characters")
    
    # Test file parsing
    print("\n🔧 Testing File Parser...")
    parser = ProjectFileParser(crew_output, project_id)
    parsed_result = parser.parse()
    
    if not parsed_result['success']:
        print(f"❌ File parsing failed: {parsed_result.get('error')}")
        print(f"📋 Parsing errors: {parsed_result.get('parsing_errors', [])}")
        return False
    
    print(f"✅ Parsed {parsed_result['file_count']} files")
    
    # Show parsed files
    print("\n📁 Parsed Files:")
    for file_path, file_info in parsed_result.get('files', {}).items():
        size = file_info.get('size', 0)
        valid = file_info.get('is_valid', False)
        status = "✅" if valid else "❌"
        print(f"   {status} {file_path} ({size} chars)")
    
    # Test project structure creation
    print("\n🏗️  Testing Project Structure Creation...")
    structure_result = create_project_structure(project_id, parsed_result)
    
    if not structure_result['success']:
        print(f"❌ Project structure creation failed")
        print(f"📋 Folder result: {structure_result.get('folder_result', {})}")
        print(f"📋 ZIP result: {structure_result.get('zip_result', {})}")
        return False
    
    print(f"✅ Created project structure with {structure_result['total_files']} files")
    print(f"📋 Templates injected: {structure_result.get('templates_injected', 0)}")
    
    # Check if files were actually created
    files_path = Path(f"generated/projects/{project_id}/files")
    if files_path.exists():
        file_count = len(list(files_path.rglob("*")))
        print(f"✅ Physical files created: {file_count}")
        
        # List some key files
        key_files = ['package.json', 'src/main.tsx', 'src/App.tsx', 'vite.config.ts']
        print("\n📋 Key Files Check:")
        for key_file in key_files:
            file_path = files_path / key_file
            if file_path.exists():
                print(f"   ✅ {key_file}")
            else:
                print(f"   ❌ {key_file} (missing)")
    else:
        print("❌ Files directory not created")
        return False
    
    print("\n🎉 SUCCESS: File parsing and structure creation working!")
    return True

if __name__ == "__main__":
    success = test_parsing()
    sys.exit(0 if success else 1)
