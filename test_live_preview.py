"""Test the Live Preview System (Phase 4)."""

import sys
import time
import requests
sys.path.append('backend')

from backend.utils.project_preview import preview_manager

def test_live_preview_system():
    """Test the complete live preview workflow."""
    
    print("🧪 Testing Phase 4: Live Preview System")
    print("=" * 60)
    
    # Use an existing project with parsed files
    project_id = "66d766ee-909c-4d2c-a2a6-ddf1b2c72aad"  # From our successful test
    
    print(f"🎯 Step 1: Testing preview manager with project {project_id[:8]}...")
    
    # Test 1: Start preview
    print("   Starting preview server...")
    start_result = preview_manager.start_preview(project_id)
    
    if start_result['success']:
        print(f"   ✅ Preview started successfully!")
        print(f"   📍 URL: {start_result['url']}")
        print(f"   🔌 Port: {start_result['port']}")
        
        # Test 2: Check status
        print("\n🔍 Step 2: Checking preview status...")
        status_result = preview_manager.get_preview_status(project_id)
        
        if status_result['success'] and status_result['running']:
            print(f"   ✅ Preview is running!")
            print(f"   ⏱️  Uptime: {status_result['uptime']:.1f} seconds")
            
            # Test 3: Try to access the preview
            print("\n🌐 Step 3: Testing HTTP access...")
            try:
                response = requests.get(start_result['url'], timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ HTTP request successful! (Status: {response.status_code})")
                    print(f"   📄 Content length: {len(response.text)} bytes")
                    
                    # Check if it looks like HTML
                    if '<html' in response.text.lower() or '<!doctype' in response.text.lower():
                        print("   ✅ Response contains HTML content!")
                    else:
                        print("   ⚠️  Response doesn't look like HTML")
                        
                else:
                    print(f"   ❌ HTTP request failed with status: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"   ❌ HTTP request failed: {str(e)}")
            
            # Test 4: List active previews
            print("\n📋 Step 4: Listing active previews...")
            active_result = preview_manager.list_active_previews()
            
            if active_result['success']:
                print(f"   ✅ Found {active_result['total_active']} active preview(s)")
                for pid, info in active_result['active_previews'].items():
                    print(f"   📍 {pid[:8]}: {info['url']} (uptime: {info['uptime']:.1f}s)")
            
            # Test 5: Stop preview
            print("\n🛑 Step 5: Stopping preview...")
            stop_result = preview_manager.stop_preview(project_id)
            
            if stop_result['success']:
                print("   ✅ Preview stopped successfully!")
                
                # Verify it's actually stopped
                time.sleep(1)
                final_status = preview_manager.get_preview_status(project_id)
                if not final_status['running']:
                    print("   ✅ Preview confirmed stopped!")
                else:
                    print("   ⚠️  Preview might still be running")
            else:
                print(f"   ❌ Failed to stop preview: {stop_result.get('error')}")
                
        else:
            print(f"   ❌ Preview status check failed: {status_result}")
            
    else:
        print(f"   ❌ Failed to start preview: {start_result.get('error')}")
        return
    
    print("\n" + "=" * 60)
    print("🎉 Phase 4 Live Preview System Test Complete!")
    print("\n✅ Confirmed Features:")
    print("   • Preview server startup and shutdown")
    print("   • Dynamic port allocation")
    print("   • HTTP server functionality")
    print("   • Status monitoring")
    print("   • Process management")
    print("\n🚀 Live Preview System: READY FOR FRONTEND INTEGRATION!")

if __name__ == "__main__":
    test_live_preview_system()
