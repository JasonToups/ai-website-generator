#!/usr/bin/env python3
"""
Test Vite-native project generation with updated CrewAI agents

This script tests that the updated agents generate Vite projects instead of CRA projects.
"""

import sys
import asyncio
import json
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from crew.website_crew import WebsiteCrew
from utils.file_parser import ProjectFileParser
from utils.project_structure import create_project_structure

async def test_vite_generation():
    """Test that CrewAI generates Vite-native projects."""
    print("🚀 Testing Vite-Native Project Generation\n")
    
    # Test project parameters
    description = "Create a modern portfolio website for a web developer"
    requirements = ["responsive design", "contact form", "project showcase"]
    style_preferences = {"theme": "modern", "colors": ["blue", "white"]}
    project_id = "test-vite-generation"
    
    try:
        # Initialize the crew
        crew = WebsiteCrew()
        print("✅ CrewAI initialized")
        
        # Generate website
        print("🎬 Starting website generation...")
        result = await crew.generate_website(
            description=description,
            requirements=requirements,
            style_preferences=style_preferences,
            project_id=project_id
        )
        
        if not result.get("success"):
            print(f"❌ Generation failed: {result.get('error')}")
            return False
        
        print("✅ Website generation completed")
        
        # Parse the output
        crew_output = str(result.get("result", ""))
        print(f"📄 Crew output length: {len(crew_output)} characters")
        
        # Parse files
        parser = ProjectFileParser(crew_output, project_id)
        parsed_result = parser.parse()
        
        if not parsed_result['success']:
            print(f"❌ File parsing failed: {parsed_result.get('error')}")
            return False
        
        print(f"✅ Parsed {parsed_result['file_count']} files")
        
        # Check for Vite-specific patterns
        vite_indicators = check_vite_patterns(parsed_result)
        
        # Create project structure with templates
        structure_result = create_project_structure(project_id, parsed_result)
        
        if not structure_result['success']:
            print(f"❌ Project structure creation failed")
            return False
        
        print(f"✅ Created project structure with {structure_result['total_files']} files")
        print(f"📋 Templates injected: {structure_result.get('templates_injected', 0)}")
        
        # Final verification
        print("\n🔍 Vite Compatibility Analysis:")
        for indicator, found in vite_indicators.items():
            status = "✅" if found else "❌"
            print(f"   {status} {indicator}")
        
        # Overall assessment
        vite_score = sum(vite_indicators.values())
        total_checks = len(vite_indicators)
        
        print(f"\n📊 Vite Compatibility Score: {vite_score}/{total_checks}")
        
        if vite_score >= total_checks * 0.8:  # 80% or better
            print("🎉 SUCCESS: Project is Vite-compatible!")
            return True
        else:
            print("⚠️  WARNING: Project may not be fully Vite-compatible")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_vite_patterns(parsed_result):
    """Check for Vite-specific patterns in the parsed files."""
    indicators = {
        "Has package.json": False,
        "Uses Vite scripts": False,
        "No react-scripts": True,  # Should NOT have react-scripts
        "Has main.tsx": False,
        "Uses modern React Router": False,
        "Has TypeScript": False,
        "Has proper imports": False
    }
    
    files = parsed_result.get('files', {})
    
    # Check package.json
    if 'package.json' in files:
        indicators["Has package.json"] = True
        
        try:
            package_content = files['package.json']['content']
            package_data = json.loads(package_content)
            
            # Check scripts
            scripts = package_data.get('scripts', {})
            if 'dev' in scripts and 'vite' in scripts['dev']:
                indicators["Uses Vite scripts"] = True
            
            # Check for react-scripts (should NOT be present)
            if 'react-scripts' in str(package_data):
                indicators["No react-scripts"] = False
            
        except json.JSONDecodeError:
            pass
    
    # Check for main.tsx
    if 'src/main.tsx' in files:
        indicators["Has main.tsx"] = True
    
    # Check for modern React Router patterns
    for file_path, file_info in files.items():
        if file_path.endswith('.tsx'):
            content = file_info.get('content', '')
            
            # Check for TypeScript
            if 'React.FC' in content or ': string' in content or 'interface ' in content:
                indicators["Has TypeScript"] = True
            
            # Check for modern React Router
            if 'Routes' in content and 'Route' in content and 'Switch' not in content:
                indicators["Uses modern React Router"] = True
            
            # Check for proper ES module imports
            if 'import React' in content and 'from ' in content:
                indicators["Has proper imports"] = True
    
    return indicators

def main():
    """Run the Vite generation test."""
    try:
        success = asyncio.run(test_vite_generation())
        return success
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
