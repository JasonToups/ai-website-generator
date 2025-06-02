"""Test script for Phase 3 API endpoints."""

import sys
import requests
import json
sys.path.append('backend')

# Test configuration
BASE_URL = "http://localhost:8000/api/v1"
PROJECT_ID = "9e5c696f-96e4-445a-8bd9-a909b0b37a33"  # Our existing test project

def test_file_tree_endpoint():
    """Test the file tree endpoint."""
    print("🌳 Testing File Tree Endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/projects/{PROJECT_ID}/files/tree")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ File tree endpoint working!")
            print(f"   Success: {data.get('success')}")
            print(f"   Total files: {data.get('total_files')}")
            print(f"   Total size: {data.get('total_size')} bytes")
            
            # Show tree structure
            tree = data.get('tree', {})
            print(f"   Root: {tree.get('name')}")
            for child in tree.get('children', [])[:3]:  # Show first 3 items
                print(f"   📁 {child.get('name')} ({child.get('type')})")
            
            return True
        else:
            print(f"❌ File tree endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the backend server running?")
        print("   Run: make backend")
        return False
    except Exception as e:
        print(f"❌ Error testing file tree: {str(e)}")
        return False

def test_individual_file_endpoint():
    """Test the individual file endpoint."""
    print("\n📄 Testing Individual File Endpoint...")
    
    try:
        # Test getting App.tsx
        file_path = "src/App.tsx"
        response = requests.get(f"{BASE_URL}/projects/{PROJECT_ID}/files/{file_path}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Individual file endpoint working!")
            print(f"   Success: {data.get('success')}")
            print(f"   File: {data.get('name')}")
            print(f"   Extension: {data.get('extension')}")
            print(f"   Size: {data.get('size')} characters")
            print(f"   Content preview: {data.get('content', '')[:100]}...")
            
            return True
        else:
            print(f"❌ Individual file endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing individual file: {str(e)}")
        return False

def test_download_endpoint():
    """Test the ZIP download endpoint."""
    print("\n📦 Testing ZIP Download Endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/projects/{PROJECT_ID}/download")
        
        if response.status_code == 200:
            print(f"✅ ZIP download endpoint working!")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            print(f"   Content-Length: {response.headers.get('content-length')} bytes")
            
            # Check if it's actually a ZIP file
            if response.headers.get('content-type') == 'application/zip':
                print(f"   ✅ Correct MIME type for ZIP file")
            else:
                print(f"   ⚠️  Unexpected MIME type: {response.headers.get('content-type')}")
            
            return True
        else:
            print(f"❌ ZIP download endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing ZIP download: {str(e)}")
        return False

def test_preview_endpoint():
    """Test the preview endpoint."""
    print("\n🖥️  Testing Preview Endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/projects/{PROJECT_ID}/preview")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Preview endpoint working!")
            print(f"   Success: {data.get('success')}")
            print(f"   Preview ready: {data.get('preview_ready')}")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            
            return True
        else:
            print(f"❌ Preview endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing preview: {str(e)}")
        return False

def test_existing_endpoints():
    """Test that existing endpoints still work."""
    print("\n🔄 Testing Existing Endpoints...")
    
    try:
        # Test project status
        response = requests.get(f"{BASE_URL}/projects/{PROJECT_ID}/status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status endpoint still working!")
            print(f"   Project ID: {data.get('project_id')}")
            print(f"   Status: {data.get('status')}")
            
            return True
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing existing endpoints: {str(e)}")
        return False

def main():
    """Run all endpoint tests."""
    print("🧪 Testing Phase 3 API Endpoints")
    print("=" * 50)
    
    results = []
    
    # Test all endpoints
    results.append(test_existing_endpoints())
    results.append(test_file_tree_endpoint())
    results.append(test_individual_file_endpoint())
    results.append(test_download_endpoint())
    results.append(test_preview_endpoint())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"   ✅ Passed: {passed}/{total}")
    print(f"   ❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All Phase 3 endpoints working perfectly!")
        print("\n📋 Available Endpoints:")
        print(f"   🌳 File Tree: GET {BASE_URL}/projects/{{id}}/files/tree")
        print(f"   📄 Individual File: GET {BASE_URL}/projects/{{id}}/files/{{path}}")
        print(f"   📦 ZIP Download: GET {BASE_URL}/projects/{{id}}/download")
        print(f"   🖥️  Preview Info: GET {BASE_URL}/projects/{{id}}/preview")
    else:
        print(f"\n⚠️  {total - passed} endpoint(s) need attention.")
        print("\nMake sure:")
        print("   1. Backend server is running (make backend)")
        print("   2. Project files exist for the test project")
        print("   3. All dependencies are installed")

if __name__ == "__main__":
    main()
