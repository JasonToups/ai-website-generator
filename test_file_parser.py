"""Test script for the file parser module."""

import sys
import os
sys.path.append('backend')

from backend.utils.file_parser import ProjectFileParser

def test_file_parser():
    """Test the file parser with existing crew output."""
    
    # Read the existing crew output
    project_id = "9e5c696f-96e4-445a-8bd9-a909b0b37a33"
    crew_output_path = f"generated/projects/{project_id}/crew_output.txt"
    
    try:
        with open(crew_output_path, 'r', encoding='utf-8') as f:
            crew_output = f.read()
        
        print(f"✅ Successfully read crew output ({len(crew_output)} characters)")
        
        # Create parser and test
        parser = ProjectFileParser(crew_output, project_id)
        
        # Test file block extraction
        file_blocks = parser.extract_file_blocks()
        print(f"✅ Extracted {len(file_blocks)} file blocks")
        
        for i, block in enumerate(file_blocks[:3]):  # Show first 3
            print(f"   {block['number']}. {block['path']} ({block['language']}) - {len(block['content'])} chars")
        
        # Test full parsing
        result = parser.parse()
        
        print(f"\n📊 Parsing Results:")
        print(f"   Files parsed: {result['file_count']}")
        print(f"   Success: {result['success']}")
        print(f"   Errors: {len(result['parsing_errors'])}")
        
        if result['parsing_errors']:
            print(f"\n❌ Parsing Errors:")
            for error in result['parsing_errors']:
                print(f"   - {error}")
        
        # Show file structure
        print(f"\n📁 Project Structure:")
        structure = result['project_structure']
        print(f"   Root: {structure['name']} ({len(structure['children'])} items)")
        
        for item in structure['children']:
            if item['type'] == 'folder':
                print(f"   📁 {item['name']} ({len(item['children'])} items)")
            else:
                print(f"   📄 {item['name']} ({item['size']} bytes)")
        
        # Show parsing summary
        summary = parser.get_parsing_summary()
        print(f"\n📈 Summary:")
        print(f"   Total files: {summary['total_files']}")
        print(f"   Valid files: {summary['valid_files']}")
        print(f"   Invalid files: {summary['invalid_files']}")
        print(f"   Success rate: {summary['success_rate']:.1f}%")
        print(f"   File types: {summary['file_types']}")
        
        return result
        
    except FileNotFoundError:
        print(f"❌ Could not find crew output file: {crew_output_path}")
        return None
    except Exception as e:
        print(f"❌ Error testing file parser: {str(e)}")
        return None

if __name__ == "__main__":
    print("🧪 Testing File Parser Module")
    print("=" * 50)
    
    result = test_file_parser()
    
    if result and result['success']:
        print("\n🎉 File parser test completed successfully!")
    else:
        print("\n⚠️  File parser test completed with issues.")
