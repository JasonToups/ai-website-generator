#!/usr/bin/env python3
"""Test script for Phase 5 Gallery implementation."""

import requests
import json

def test_gallery_functionality():
    """Test the complete gallery functionality."""
    print("🎨 Testing Phase 5 Gallery Implementation\n")
    
    # Test 1: Gallery API
    print("1. Testing Gallery API...")
    try:
        response = requests.get("http://localhost:8000/api/v1/projects/gallery")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Gallery API working! Found {data['total']} projects")
            
            if data['projects']:
                project = data['projects'][0]
                print(f"   📋 Sample project: {project['title']}")
                print(f"   🏷️ Type: {project['metadata']['website_type']}")
                print(f"   📁 Files: {project['file_count']}")
                print(f"   🔧 Tech: {', '.join(project['metadata']['technologies'])}")
        else:
            print(f"   ❌ Gallery API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: Project deletion endpoint
    print("\n2. Testing Project Deletion Endpoint...")
    try:
        # Just test that the endpoint exists (don't actually delete)
        response = requests.delete("http://localhost:8000/api/v1/projects/nonexistent-id")
        if response.status_code == 404:
            print("   ✅ Delete endpoint working (404 for non-existent project)")
        else:
            print(f"   ⚠️ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 3: Thumbnail endpoint
    print("\n3. Testing Thumbnail Endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/v1/projects/test-id/thumbnail")
        if response.status_code == 200:
            print("   ✅ Thumbnail endpoint working (placeholder)")
        else:
            print(f"   ⚠️ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n🎉 Phase 5 Backend Testing Complete!")
    print("\n📋 Next Steps:")
    print("   1. Visit http://localhost:3000 in your browser")
    print("   2. Click on the 'Gallery' tab")
    print("   3. You should see all your generated projects in a beautiful grid")
    print("   4. Try the Preview, Download, and Delete buttons")
    print("   5. Test the search and filter functionality")

if __name__ == "__main__":
    test_gallery_functionality()
