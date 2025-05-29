#!/usr/bin/env python3
"""Test script for the new gallery API endpoint."""

import requests
import json

def test_gallery_api():
    """Test the gallery API endpoint."""
    try:
        # Test gallery endpoint
        print("🧪 Testing Gallery API...")
        response = requests.get("http://localhost:8000/api/v1/projects/gallery")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Gallery API working! Found {data['total']} projects")
            
            # Show first project details
            if data['projects']:
                project = data['projects'][0]
                print(f"\n📋 Sample Project:")
                print(f"   Title: {project['title']}")
                print(f"   Type: {project['metadata']['website_type']}")
                print(f"   Files: {project['file_count']}")
                print(f"   Technologies: {', '.join(project['metadata']['technologies'])}")
                print(f"   Preview Available: {project['has_preview']}")
        else:
            print(f"❌ Gallery API failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing gallery API: {str(e)}")

def test_health():
    """Test basic health endpoint."""
    try:
        print("🏥 Testing Health endpoint...")
        response = requests.get("http://localhost:8000/health")
        
        if response.status_code == 200:
            print("✅ Backend is healthy!")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing health: {str(e)}")

if __name__ == "__main__":
    print("🚀 Testing Phase 5 Gallery API Implementation\n")
    test_health()
    print()
    test_gallery_api()
    print("\n✨ Test complete!")
