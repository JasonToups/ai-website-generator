#!/usr/bin/env python3
"""
Debug script to test regex patterns on the new crew output
"""

import re
from pathlib import Path

def test_regex_patterns():
    """Test different regex patterns on the crew output."""
    print("🔍 Testing Regex Patterns on Crew Output\n")
    
    # Read the crew output
    project_id = "16fdd748-a31a-488b-9df9-882d6e77d588"
    crew_output_path = Path(f"generated/projects/{project_id}/crew_output.txt")
    
    with open(crew_output_path, 'r', encoding='utf-8') as f:
        crew_output = f.read()
    
    print(f"📄 Crew output length: {len(crew_output)} characters")
    
    # Show first 1000 characters to see the format
    print("\n📋 First 1000 characters:")
    print("=" * 50)
    print(crew_output[:1000])
    print("=" * 50)
    
    # Test current pattern
    print("\n🔧 Testing Current Pattern:")
    current_pattern = r'(\d+)\.\s+([^\n]+)\n\n```(\w+)\n(.*?)\n```'
    current_matches = re.findall(current_pattern, crew_output, re.DOTALL)
    print(f"Current pattern matches: {len(current_matches)}")
    
    # Test alternative patterns
    patterns = [
        # Pattern 1: File path followed by colon and code block
        (r'([^:]+):\n\n```(\w+)\n(.*?)\n```', "File path with colon"),
        
        # Pattern 2: File path without number
        (r'([^\n]+\.(?:tsx|ts|jsx|js|json|md|css)):\n\n```(\w+)\n(.*?)\n```', "File extension based"),
        
        # Pattern 3: More flexible pattern
        (r'([^\n]*(?:src/|\.)[^\n]*?):\n\n```(\w+)\n(.*?)\n```', "Flexible file pattern"),
        
        # Pattern 4: Look for any file-like pattern
        (r'([^\n]+\.[a-zA-Z]+):\n\n```(\w+)\n(.*?)\n```', "Any file extension"),
    ]
    
    for pattern, description in patterns:
        print(f"\n🧪 Testing: {description}")
        print(f"Pattern: {pattern}")
        matches = re.findall(pattern, crew_output, re.DOTALL)
        print(f"Matches found: {len(matches)}")
        
        if matches:
            print("First few matches:")
            for i, match in enumerate(matches[:3]):
                if len(match) >= 3:
                    file_path = match[0].strip()
                    language = match[1].strip()
                    content_preview = match[2][:100].strip()
                    print(f"  {i+1}. {file_path} ({language}) - {len(match[2])} chars")
                    print(f"     Preview: {content_preview}...")
    
    # Look for specific patterns in the text
    print("\n🔍 Looking for specific patterns:")
    
    # Check for file paths
    file_patterns = [
        r'src/[^\n:]+\.tsx?',
        r'[^\n]*\.json',
        r'[^\n]*\.md',
        r'package\.json',
        r'README\.md'
    ]
    
    for pattern in file_patterns:
        matches = re.findall(pattern, crew_output)
        if matches:
            print(f"Found {pattern}: {matches[:3]}")

if __name__ == "__main__":
    test_regex_patterns()
