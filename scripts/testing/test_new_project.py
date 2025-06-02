"""Test the new project parsing."""

import sys
sys.path.append('backend')

from backend.utils.file_parser import ProjectFileParser
from backend.utils.project_structure import create_project_structure

def test_new_project():
    project_id = '3ec68bde-f4ee-4d3b-b2e9-6a6d55443de1'
    
    print('🔍 Testing automatic parsing on new project...')
    
    # Read the crew output
    with open(f'generated/projects/{project_id}/crew_output.txt', 'r') as f:
        crew_output = f.read()
    
    print(f'Crew output length: {len(crew_output)} characters')
    
    # Parse files
    parser = ProjectFileParser(crew_output, project_id)
    parsed_result = parser.parse()
    
    print(f'Parse success: {parsed_result["success"]}')
    if parsed_result['success']:
        print(f'Files found: {len(parsed_result["files"])}')
        
        # Create structure
        structure_result = create_project_structure(project_id, parsed_result)
        print(f'Structure success: {structure_result["success"]}')
        if structure_result['success']:
            print(f'Total files created: {structure_result["total_files"]}')
            print('✅ Manual parsing worked!')
        else:
            print(f'Structure error: {structure_result.get("error")}')
    else:
        print(f'Parse error: {parsed_result.get("error")}')

if __name__ == "__main__":
    test_new_project()
