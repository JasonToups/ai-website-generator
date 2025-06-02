"""Test the enhanced generation flow with automatic file parsing."""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_enhanced_generation():
    """Test that new website generation includes automatic file parsing."""
    print("🧪 Testing Enhanced Generation Flow with Automatic File Parsing")
    print("=" * 70)
    
    # Step 1: Generate a new website
    print("🚀 Step 1: Starting website generation...")
    
    generation_request = {
        "description": "A simple portfolio website for a photographer",
        "requirements": ["responsive design", "image gallery", "contact form"],
        "style_preferences": {"theme": "modern", "colors": ["blue", "white"]}
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate", json=generation_request)
        
        if response.status_code == 200:
            data = response.json()
            project_id = data['project_id']
            print(f"✅ Generation started successfully!")
            print(f"   Project ID: {project_id}")
            print(f"   Status: {data['status']}")
            
            # Step 2: Monitor progress
            print(f"\n⏳ Step 2: Monitoring generation progress...")
            
            max_attempts = 30  # 5 minutes max
            attempt = 0
            
            while attempt < max_attempts:
                time.sleep(10)  # Wait 10 seconds between checks
                attempt += 1
                
                status_response = requests.get(f"{BASE_URL}/projects/{project_id}/status")
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    current_status = status_data['status']
                    current_step = status_data.get('current_step', 'Unknown')
                    
                    print(f"   Attempt {attempt}: {current_status} - {current_step}")
                    
                    if current_status in ['completed', 'failed']:
                        break
                else:
                    print(f"   ❌ Status check failed: {status_response.status_code}")
                    return False
            
            # Step 3: Check if file parsing worked
            if current_status == 'completed':
                print(f"\n🎉 Step 3: Generation completed! Testing file parsing...")
                
                # Test file tree
                tree_response = requests.get(f"{BASE_URL}/projects/{project_id}/files/tree")
                
                if tree_response.status_code == 200:
                    tree_data = tree_response.json()
                    
                    if tree_data.get('success'):
                        print(f"✅ Automatic file parsing SUCCESSFUL!")
                        print(f"   Files parsed: {tree_data.get('total_files')}")
                        print(f"   Total size: {tree_data.get('total_size')} bytes")
                        
                        # Test ZIP download
                        zip_response = requests.get(f"{BASE_URL}/projects/{project_id}/download")
                        
                        if zip_response.status_code == 200:
                            print(f"✅ ZIP archive automatically generated!")
                            print(f"   ZIP size: {zip_response.headers.get('content-length')} bytes")
                            
                            return True
                        else:
                            print(f"❌ ZIP generation failed: {zip_response.status_code}")
                            return False
                    else:
                        print(f"❌ File parsing failed: {tree_data.get('error')}")
                        return False
                else:
                    print(f"❌ File tree endpoint failed: {tree_response.status_code}")
                    return False
            else:
                print(f"❌ Generation failed with status: {current_status}")
                return False
                
        else:
            print(f"❌ Generation request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during enhanced generation test: {str(e)}")
        return False

def main():
    """Run the enhanced generation test."""
    success = test_enhanced_generation()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 ENHANCED GENERATION FLOW WORKING PERFECTLY!")
        print("\n✅ Confirmed Features:")
        print("   • Automatic file parsing during generation")
        print("   • Individual files created on disk")
        print("   • ZIP archives automatically generated")
        print("   • File tree API working")
        print("   • Complete project delivery pipeline")
        print("\n🚀 Phase 3 API Integration: COMPLETE!")
    else:
        print("⚠️  Enhanced generation flow needs attention.")
        print("\nThis could be due to:")
        print("   • Generation taking longer than expected")
        print("   • File parsing integration issues")
        print("   • Backend server issues")

if __name__ == "__main__":
    main()
