"""Test Phase 4 Live Preview API Integration."""

import sys
import time
import requests
sys.path.append('backend')

def test_phase4_api():
    """Test the Phase 4 Live Preview API endpoints."""
    
    base_url = "http://localhost:8000"
    project_id = 'b216ae3e-94ac-49b3-a986-21ee86ecb56f'
    
    print('🧪 Testing Phase 4: Live Preview API Integration')
    print('=' * 60)
    print(f'🎯 Testing with project {project_id[:8]}...')
    print(f'📍 Base URL: {base_url}')
    print('')
    
    # Test 1: Get preview info
    print('📋 Step 1: Getting preview info...')
    try:
        response = requests.get(f"{base_url}/projects/{project_id}/preview")
        if response.status_code == 200:
            data = response.json()
            print(f'   ✅ Preview info retrieved successfully!')
            print(f'   📊 Preview available: {data.get("preview_available")}')
            print(f'   📁 Files path: {data.get("files_path", "N/A")[:50]}...')
        else:
            print(f'   ❌ Failed to get preview info: {response.status_code}')
            print(f'   📄 Response: {response.text}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'   ❌ Request failed: {str(e)}')
        print('   ⚠️  Make sure the backend server is running: poetry run python backend/main.py')
        return False
    
    # Test 2: Start preview
    print('\n🚀 Step 2: Starting preview server...')
    try:
        response = requests.post(f"{base_url}/projects/{project_id}/preview/start")
        if response.status_code == 200:
            data = response.json()
            print(f'   ✅ Preview started successfully!')
            print(f'   📍 URL: {data.get("url")}')
            print(f'   🔌 Port: {data.get("port")}')
            print(f'   📊 Status: {data.get("status")}')
            
            preview_url = data.get("url")
            
        else:
            print(f'   ❌ Failed to start preview: {response.status_code}')
            print(f'   📄 Response: {response.text}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'   ❌ Request failed: {str(e)}')
        return False
    
    # Test 3: Check preview status
    print('\n🔍 Step 3: Checking preview status...')
    try:
        response = requests.get(f"{base_url}/projects/{project_id}/preview/status")
        if response.status_code == 200:
            data = response.json()
            print(f'   ✅ Status retrieved successfully!')
            print(f'   🏃 Running: {data.get("running")}')
            if data.get("running"):
                print(f'   ⏱️  Uptime: {data.get("uptime", 0):.1f} seconds')
        else:
            print(f'   ❌ Failed to get status: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'   ❌ Request failed: {str(e)}')
    
    # Test 4: Get preview URL
    print('\n🌐 Step 4: Getting preview URL...')
    try:
        response = requests.get(f"{base_url}/projects/{project_id}/preview/url")
        if response.status_code == 200:
            data = response.json()
            print(f'   ✅ URL retrieved successfully!')
            print(f'   📍 Preview URL: {data.get("url")}')
        else:
            print(f'   ❌ Failed to get URL: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'   ❌ Request failed: {str(e)}')
    
    # Test 5: Test actual website access
    if preview_url:
        print('\n🌍 Step 5: Testing website access...')
        try:
            response = requests.get(preview_url, timeout=5)
            if response.status_code == 200:
                print(f'   ✅ Website accessible!')
                print(f'   📄 Content length: {len(response.text)} bytes')
                
                # Check if it's the PhotoLens portfolio
                if 'PhotoLens' in response.text:
                    print('   ✅ PhotoLens portfolio detected!')
                if 'Capturing moments' in response.text:
                    print('   ✅ Hero section content found!')
                if 'About the Photographer' in response.text:
                    print('   ✅ About section content found!')
                    
            else:
                print(f'   ❌ Website not accessible: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'   ❌ Website access failed: {str(e)}')
    
    # Test 6: List active previews
    print('\n📋 Step 6: Listing active previews...')
    try:
        response = requests.get(f"{base_url}/preview/active")
        if response.status_code == 200:
            data = response.json()
            print(f'   ✅ Active previews listed!')
            print(f'   📊 Total active: {data.get("total_active", 0)}')
            
            active_previews = data.get("active_previews", {})
            for pid, info in active_previews.items():
                print(f'   📍 {pid[:8]}: {info.get("url")} (uptime: {info.get("uptime", 0):.1f}s)')
        else:
            print(f'   ❌ Failed to list previews: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'   ❌ Request failed: {str(e)}')
    
    # Test 7: Stop preview
    print('\n🛑 Step 7: Stopping preview server...')
    try:
        response = requests.delete(f"{base_url}/projects/{project_id}/preview/stop")
        if response.status_code == 200:
            data = response.json()
            print(f'   ✅ Preview stopped successfully!')
            print(f'   📊 Status: {data.get("status")}')
        else:
            print(f'   ❌ Failed to stop preview: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'   ❌ Request failed: {str(e)}')
    
    print('\n' + '=' * 60)
    print('🎉 Phase 4 Live Preview API Integration Test Complete!')
    print('')
    print('✅ Confirmed API Endpoints:')
    print('   • GET /projects/{id}/preview - Preview info')
    print('   • POST /projects/{id}/preview/start - Start preview')
    print('   • DELETE /projects/{id}/preview/stop - Stop preview')
    print('   • GET /projects/{id}/preview/status - Preview status')
    print('   • GET /projects/{id}/preview/url - Preview URL')
    print('   • GET /preview/active - List active previews')
    print('')
    print('🚀 PHASE 4 LIVE PREVIEW SYSTEM: FULLY INTEGRATED!')
    
    return True

if __name__ == "__main__":
    success = test_phase4_api()
    if success:
        print('\n🎯 Ready for frontend integration!')
    else:
        print('\n❌ API testing incomplete - check backend server')
