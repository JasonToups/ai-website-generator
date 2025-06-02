"""Debug the file parsing issue with the new project."""

import sys
sys.path.append('backend')

from backend.utils.file_parser import ProjectFileParser
from backend.utils.project_structure import create_project_structure

def debug_parsing():
    project_id = 'b216ae3e-94ac-49b3-a986-21ee86ecb56f'
    
    print("🔍 Debugging file parsing for new project...")
    print(f"Project ID: {project_id}")
    
    # Read the crew output
    try:
        with open(f'generated/projects/{project_id}/crew_output.txt', 'r') as f:
            crew_output = f.read()
        
        print(f"✅ Crew output loaded: {len(crew_output)} characters")
        
        # Parse files
        parser = ProjectFileParser(crew_output, project_id)
        parsed_result = parser.parse()
        
        print(f"Parse success: {parsed_result['success']}")
        
        if parsed_result['success']:
            files = parsed_result['files']
            print(f"Files found: {len(files)}")
            print(f"Files type: {type(files)}")
            
            # Debug: Check the structure
            if isinstance(files, dict):
                print("Files is a dictionary with keys:")
                for key in list(files.keys())[:3]:
                    print(f"  - {key}: {type(files[key])}")
            elif isinstance(files, list):
                print("Files is a list:")
                for i, file_info in enumerate(files[:3]):
                    print(f"  - {i}: {file_info}")
            
            # Create structure
            print("\n🏗️  Creating project structure...")
            structure_result = create_project_structure(project_id, parsed_result)
            
            print(f"Structure success: {structure_result['success']}")
            if structure_result['success']:
                print(f"Total files created: {structure_result['total_files']}")
                print(f"ZIP created: {structure_result.get('zip_created', False)}")
                
                # Test the new endpoints
                print("\n🧪 Testing new endpoints...")
                from backend.utils.project_structure import ProjectStructureManager
                
                manager = ProjectStructureManager(project_id)
                
                # Test file tree
                tree_result = manager.get_file_tree()
                print(f"File tree: {tree_result['success']}")
                
                # Test individual file
                file_result = manager.get_individual_file('src/App.tsx')
                print(f"Individual file: {file_result['success']}")
                
                print("\n🎉 All tests passed! Phase 3 integration working!")
                
            else:
                print(f"Structure error: {structure_result.get('error')}")
        else:
            print(f"Parse error: {parsed_result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_parsing()
