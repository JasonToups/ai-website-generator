#!/usr/bin/env python3
"""Test script for Phase 6 React Router implementation."""

import requests
import time

def test_phase6_implementation():
    """Test the complete Phase 6 React Router implementation."""
    print("🚀 Testing Phase 6 React Router Implementation\n")
    
    # Test 1: Backend API endpoints
    print("1. Testing Backend API Endpoints...")
    try:
        # Test preview content endpoint
        response = requests.get("http://localhost:8000/api/v1/projects/b216ae3e-94ac-49b3-a986-21ee86ecb56f/preview-content")
        if response.status_code == 200:
            print("   ✅ Preview content endpoint working!")
            print(f"   📄 Content type: {response.headers.get('content-type')}")
            print(f"   📏 Content length: {len(response.text)} characters")
        else:
            print(f"   ❌ Preview content failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: Asset serving endpoint
    print("\n2. Testing Asset Serving Endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/v1/projects/b216ae3e-94ac-49b3-a986-21ee86ecb56f/assets/src/index.css")
        if response.status_code == 200:
            print("   ✅ Asset serving working!")
            print(f"   📄 Content type: {response.headers.get('content-type')}")
        else:
            print(f"   ❌ Asset serving failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 3: Gallery API (should still work)
    print("\n3. Testing Gallery API Integration...")
    try:
        response = requests.get("http://localhost:8000/api/v1/projects/gallery")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Gallery API working! Found {data['total']} projects")
        else:
            print(f"   ❌ Gallery API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n🎉 Phase 6 Backend Testing Complete!")
    print("\n📋 Next Steps:")
    print("   1. Visit http://localhost:3000 in your browser")
    print("   2. Navigate to the Gallery tab")
    print("   3. Click the 'Preview' button on any project")
    print("   4. You should see the project preview in-app (not a new tab)")
    print("   5. Use the 'Back to Gallery' button to return")
    print("   6. Test the navigation between Gallery and Dashboard tabs")
    
    print("\n🔧 Expected Behavior:")
    print("   ✅ Preview opens at /preview/project-id URL")
    print("   ✅ Project content loads in iframe")
    print("   ✅ No external browser tabs opened")
    print("   ✅ Seamless navigation back to gallery")
    print("   ✅ Tab navigation still works")

if __name__ == "__main__":
    test_phase6_implementation()
