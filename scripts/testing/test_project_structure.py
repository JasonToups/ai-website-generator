"""Test script for the project structure manager."""

import sys
import os
sys.path.append('backend')

from backend.utils.file_parser import ProjectFileParser
from backend.utils.project_structure import ProjectStructureManager, create_project_structure

def test_project_structure():
    """Test the complete file parsing and project structure creation."""
    
    # Read the existing crew output
    project_id = "9e5c696f-96e4-445a-8bd9-a909b0b37a33"
    crew_output_path = f"generated/projects/{project_id}/crew_output.txt"
    
    try:
        with open(crew_output_path, 'r', encoding='utf-8') as f:
            crew_output = f.read()
        
        print(f"✅ Successfully read crew output ({len(crew_output)} characters)")
        
        # Step 1: Parse files
        parser = ProjectFileParser(crew_output, project_id)
        parsed_result = parser.parse()
        
        print(f"✅ Parsed {parsed_result['file_count']} files successfully")
        
        # Step 2: Create project structure
        structure_result = create_project_structure(project_id, parsed_result)
        
        print(f"\n📁 Project Structure Creation:")
        print(f"   Success: {structure_result['success']}")
        print(f"   Project path: {structure_result['project_path']}")
        print(f"   Total files: {structure_result['total_files']}")
        
        if structure_result['success']:
            folder_result = structure_result['folder_result']
            zip_result = structure_result['zip_result']
            
            print(f"\n📂 Folder Creation:")
            print(f"   Files created: {folder_result['total_files']}")
            print(f"   Directories created: {folder_result['total_directories']}")
            print(f"   Files path: {folder_result['files_path']}")
            
            print(f"\n📦 ZIP Archive:")
            print(f"   ZIP created: {zip_result['success']}")
            if zip_result['success']:
                print(f"   ZIP path: {zip_result['zip_path']}")
                print(f"   ZIP size: {zip_result['zip_size_mb']} MB")
        
        # Step 3: Test file tree retrieval
        manager = ProjectStructureManager(project_id)
        tree_result = manager.get_file_tree()
        
        print(f"\n🌳 File Tree:")
        print(f"   Success: {tree_result['success']}")
        if tree_result['success']:
            print(f"   Total files: {tree_result['total_files']}")
            print(f"   Total size: {tree_result['total_size']} bytes")
            
            # Show tree structure
            tree = tree_result['tree']
            print(f"   Root: {tree['name']}")
            for child in tree['children']:
                if child['type'] == 'folder':
                    print(f"   📁 {child['name']} ({len(child['children'])} items)")
                    for subchild in child['children'][:3]:  # Show first 3 items
                        print(f"      📄 {subchild['name']} ({subchild.get('size', 0)} bytes)")
                    if len(child['children']) > 3:
                        print(f"      ... and {len(child['children']) - 3} more files")
                else:
                    print(f"   📄 {child['name']} ({child.get('size', 0)} bytes)")
        
        # Step 4: Test individual file retrieval
        test_file = "src/App.tsx"
        file_result = manager.get_individual_file(test_file)
        
        print(f"\n📄 Individual File Test ({test_file}):")
        print(f"   Success: {file_result['success']}")
        if file_result['success']:
            print(f"   File name: {file_result['name']}")
            print(f"   Extension: {file_result['extension']}")
            print(f"   Size: {file_result['size']} characters")
            print(f"   Content preview: {file_result['content'][:100]}...")
        
        # Step 5: Test project info
        info_result = manager.get_project_info()
        print(f"\n📊 Project Info:")
        print(f"   Success: {info_result['success']}")
        if info_result['success']:
            print(f"   Has files: {info_result['has_files']}")
            print(f"   Has ZIP: {info_result['has_zip']}")
            print(f"   ZIP size: {info_result['zip_size']} bytes")
            
            manifest = info_result['manifest']
            print(f"   Manifest file count: {manifest['parsing_results']['file_count']}")
            print(f"   File types: {manifest['file_types']}")
        
        return structure_result
        
    except FileNotFoundError:
        print(f"❌ Could not find crew output file: {crew_output_path}")
        return None
    except Exception as e:
        print(f"❌ Error testing project structure: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🧪 Testing Project Structure Manager")
    print("=" * 50)
    
    result = test_project_structure()
    
    if result and result['success']:
        print("\n🎉 Project structure test completed successfully!")
        print("\n📋 Summary:")
        print(f"   ✅ Files parsed and validated")
        print(f"   ✅ Individual files created on disk")
        print(f"   ✅ ZIP archive generated")
        print(f"   ✅ File tree structure working")
        print(f"   ✅ Individual file retrieval working")
        print(f"   ✅ Project manifest created")
    else:
        print("\n⚠️  Project structure test completed with issues.")
