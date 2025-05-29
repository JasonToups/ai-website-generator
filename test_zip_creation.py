"""Quick test for ZIP creation."""

import sys
sys.path.append('backend')

from backend.utils.project_structure import ProjectStructureManager

def test_zip_creation():
    project_id = "9e5c696f-96e4-445a-8bd9-a909b0b37a33"
    manager = ProjectStructureManager(project_id)
    
    print("🧪 Testing ZIP creation...")
    result = manager.create_zip_archive()
    
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"ZIP path: {result['zip_path']}")
        print(f"ZIP size: {result['zip_size_mb']} MB")
    else:
        print(f"Error: {result['error']}")
    
    return result

if __name__ == "__main__":
    test_zip_creation()
